"""
Tests for the Frobenius census of palindromic polynomials.

Verifies:
1. Palindromic property for all fields in the extended database
2. Galois group detection matches known values for degree-5 fields
3. Frobenius traces are correct at small primes for known cases
4. Census pipeline runs and produces expected number of entries
5. All non-solvable cases have degree >= 5
"""
import pytest
from planetary_polygons.extensions.palindromic_census import (
    palindromic_from_minpoly, verify_palindromic,
    factor_degree_pattern, classify_galois_degree5,
    classify_galois_generic, collect_cycle_types,
    poly_discriminant, poly_deg, _primes_up_to,
    poly_eval, is_perfect_square,
)
from planetary_polygons.extensions.frobenius_census import (
    EXTENDED_TOTALLY_REAL_FIELDS,
    frobenius_trace_from_pattern,
    compute_frobenius_data,
    frobenius_trace_sequence,
    run_full_census,
    langlands_test_cases,
    frobenius_table,
    frobenius_statistics,
    _compute_entry,
)


# ============================================================
# Database integrity
# ============================================================

class TestDatabaseIntegrity:
    """Tests that the extended field database is well-formed."""

    def test_database_has_50_plus_entries(self):
        """Extended database should contain at least 50 fields."""
        assert len(EXTENDED_TOTALLY_REAL_FIELDS) >= 50

    def test_all_entries_have_correct_format(self):
        """Each entry is (label, degree, poly_asc, known_galois)."""
        for entry in EXTENDED_TOTALLY_REAL_FIELDS:
            assert len(entry) == 4, f"Entry has {len(entry)} fields: {entry[0]}"
            label, degree, poly_asc, known_galois = entry
            assert isinstance(label, str)
            assert isinstance(degree, int) and degree >= 1
            assert isinstance(poly_asc, list)
            assert isinstance(known_galois, str)

    def test_all_polynomials_are_monic(self):
        """Every polynomial in the database has leading coefficient 1."""
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            assert poly_asc[-1] == 1, (
                f"{label}: leading coeff = {poly_asc[-1]}, expected 1")

    def test_all_polynomials_match_degree(self):
        """Polynomial degree matches declared field degree."""
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            assert poly_deg(poly_asc) == degree, (
                f"{label}: poly degree {poly_deg(poly_asc)} != "
                f"declared degree {degree}")

    def test_all_labels_unique(self):
        """No duplicate labels."""
        labels = [entry[0] for entry in EXTENDED_TOTALLY_REAL_FIELDS]
        assert len(labels) == len(set(labels)), "Duplicate labels found"

    def test_degree_distribution(self):
        """Database should have fields of degrees 5, 6, 7, 8."""
        degrees = set(entry[1] for entry in EXTENDED_TOTALLY_REAL_FIELDS)
        assert 5 in degrees, "No degree-5 fields"
        assert 6 in degrees, "No degree-6 fields"
        assert 7 in degrees, "No degree-7 fields"
        assert 8 in degrees, "No degree-8 fields"

    def test_discriminant_matches_label(self):
        """For every entry, the computed discriminant matches the label.

        This is the critical integrity check: the LMFDB-style label
        encodes the discriminant, and it must match what poly_discriminant
        computes from the polynomial coefficients.
        """
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            disc = poly_discriminant(poly_asc)
            # Extract discriminant from label: "d.sig.disc.index"
            parts = label.split('.')
            assert len(parts) == 4, f"{label}: bad label format"
            claimed_disc = int(parts[2])
            assert disc == claimed_disc, (
                f"{label}: computed disc = {disc}, label claims {claimed_disc}")


# ============================================================
# Palindromic property for all extended fields
# ============================================================

class TestPalindromicProperty:
    """Verify palindromic polynomial construction for all extended fields."""

    def test_all_palindromic(self):
        """Every palindromic polynomial from the extended database is
        actually palindromic: Q[i] = Q[n-i] for all i."""
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            Q = palindromic_from_minpoly(poly_asc)
            assert verify_palindromic(Q), (
                f"{label}: Q is not palindromic, coeffs = {Q}")

    def test_degree_doubling(self):
        """Palindromic polynomial has degree exactly 2 * trace field degree."""
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            Q = palindromic_from_minpoly(poly_asc)
            assert poly_deg(Q) == 2 * degree, (
                f"{label}: deg(Q) = {poly_deg(Q)} != 2*{degree}")

    def test_constant_term_one(self):
        """Monic trace polynomial always gives Q with constant term 1."""
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            Q = palindromic_from_minpoly(poly_asc)
            assert Q[0] == 1, f"{label}: constant term = {Q[0]}"

    def test_leading_coeff_one(self):
        """Monic trace polynomial always gives monic Q."""
        for label, degree, poly_asc, gal in EXTENDED_TOTALLY_REAL_FIELDS:
            Q = palindromic_from_minpoly(poly_asc)
            assert Q[-1] == 1, f"{label}: leading coeff = {Q[-1]}"

    def test_quintic_palindromic_degree10(self):
        """All degree-5 fields produce degree-10 palindromic polynomials."""
        quintics = [e for e in EXTENDED_TOTALLY_REAL_FIELDS if e[1] == 5]
        assert len(quintics) >= 10
        for label, degree, poly_asc, gal in quintics:
            Q = palindromic_from_minpoly(poly_asc)
            assert poly_deg(Q) == 10, f"{label}: deg(Q) = {poly_deg(Q)}"

    def test_sextic_palindromic_degree12(self):
        """All degree-6 fields produce degree-12 palindromic polynomials."""
        sextics = [e for e in EXTENDED_TOTALLY_REAL_FIELDS if e[1] == 6]
        assert len(sextics) >= 2
        for label, degree, poly_asc, gal in sextics:
            Q = palindromic_from_minpoly(poly_asc)
            assert poly_deg(Q) == 12, f"{label}: deg(Q) = {poly_deg(Q)}"


# ============================================================
# Galois group detection for degree-5 fields
# ============================================================

class TestGaloisDetection:
    """Verify Galois group detection matches known values."""

    def test_c5_detected(self):
        """C_5 quintic (disc 14641) is correctly classified."""
        f = [1, 3, -3, -4, 1, 1]  # x^5+x^4-4x^3-3x^2+3x+1
        group = classify_galois_degree5(f, 500)
        assert group == 'C_5'

    def test_d5_detected(self):
        """D_5 quintic (disc 160801) is correctly classified."""
        f = [-1, 3, 4, -5, -1, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'D_5'

    def test_s5_38569_detected(self):
        """S_5 quintic (disc 38569) is correctly classified."""
        f = [-1, 4, 0, -5, 0, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_s5_24217_detected(self):
        """S_5 quintic (disc 24217) is correctly classified."""
        f = [1, 3, -1, -5, 0, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_s5_65657_detected(self):
        """S_5 quintic (disc 65657) is correctly classified."""
        f = [1, 5, 2, -5, -1, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_s5_245_detected(self):
        """S_5 quintic (disc 245, smallest in database) is correctly classified."""
        f = [-1, 1, 4, -2, -2, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_s5_36497_detected(self):
        """S_5 quintic (disc 36497) is correctly classified."""
        f = [-1, 1, 5, -3, -2, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_all_quintic_galois_consistent(self):
        """For all quintic fields, detected Galois group is in the expected set."""
        valid_groups = {'C_5', 'D_5', 'F_20', 'A_5', 'S_5'}
        quintics = [e for e in EXTENDED_TOTALLY_REAL_FIELDS if e[1] == 5]
        for label, degree, poly_asc, known_gal in quintics:
            detected = classify_galois_degree5(poly_asc, 500)
            assert detected in valid_groups, (
                f"{label}: got {detected}, expected one of {valid_groups}")

    def test_known_s5_are_nonsolvable(self):
        """All fields marked S_5 in the database are detected as non-solvable."""
        s5_fields = [e for e in EXTENDED_TOTALLY_REAL_FIELDS
                     if e[3] == 'S_5' and e[1] == 5]
        assert len(s5_fields) >= 5, "Need at least 5 known S_5 fields"
        for label, degree, poly_asc, known_gal in s5_fields:
            info = classify_galois_generic(poly_asc, 300)
            assert info['solvable'] is False, (
                f"{label}: expected non-solvable, got {info}")


# ============================================================
# Frobenius trace computation
# ============================================================

class TestFrobeniusTrace:
    """Verify Frobenius trace computation."""

    def test_trace_all_split(self):
        """Fully split pattern (1,1,...,1) gives trace = d-1."""
        assert frobenius_trace_from_pattern((1, 1, 1, 1, 1), 5) == 4

    def test_trace_irreducible(self):
        """Irreducible pattern (d,) gives trace = -1."""
        assert frobenius_trace_from_pattern((5,), 5) == -1

    def test_trace_mixed(self):
        """Pattern (1, 1, 3) gives trace = 1."""
        assert frobenius_trace_from_pattern((1, 1, 3), 5) == 1

    def test_trace_two_plus_three(self):
        """Pattern (2, 3) gives trace = -1."""
        assert frobenius_trace_from_pattern((2, 3), 5) == -1

    def test_trace_quadratic(self):
        """For a quadratic, (1,1) -> trace 1, (2,) -> trace -1."""
        assert frobenius_trace_from_pattern((1, 1), 2) == 1
        assert frobenius_trace_from_pattern((2,), 2) == -1

    def test_trace_for_c5_at_unramified_prime(self):
        """C_5 field: for primes p != 11, check Frobenius trace is sensible."""
        f = [1, 3, -3, -4, 1, 1]  # C_5, disc = 14641 = 11^4
        # For C_5, only patterns (1,1,1,1,1) and (5,) occur
        data = compute_frobenius_data(f, prime_bound=50)
        for p, info in data.items():
            assert info['trace'] in (-1, 4), (
                f"C_5 at p={p}: trace={info['trace']}, "
                f"pattern={info['pattern']}")


# ============================================================
# Frobenius data computation
# ============================================================

class TestFrobeniusData:
    """Test Frobenius data computation for specific fields."""

    def test_frobenius_data_keys(self):
        """Frobenius data dict has correct keys."""
        f = [-1, 4, 0, -5, 0, 1]  # S_5, disc 38569
        data = compute_frobenius_data(f, prime_bound=30)
        for p, info in data.items():
            assert 'pattern' in info
            assert 'trace' in info
            assert 'num_roots' in info
            assert 'num_factors' in info

    def test_frobenius_data_consistency(self):
        """Pattern degrees sum to polynomial degree."""
        f = [-1, 4, 0, -5, 0, 1]  # degree 5
        data = compute_frobenius_data(f, prime_bound=100)
        for p, info in data.items():
            assert sum(info['pattern']) == 5, (
                f"p={p}: pattern {info['pattern']} doesn't sum to 5")

    def test_frobenius_palindromic_consistency(self):
        """Frobenius data for palindromic Q has correct degree sum."""
        f = [-1, 4, 0, -5, 0, 1]
        Q = palindromic_from_minpoly(f)
        data = compute_frobenius_data(Q, prime_bound=50)
        for p, info in data.items():
            assert sum(info['pattern']) == 10, (
                f"p={p}: palindromic pattern {info['pattern']} "
                f"doesn't sum to 10")

    def test_frobenius_trace_sequence_length(self):
        """Trace sequence returns one entry per prime."""
        f = [1, 3, -3, -4, 1, 1]
        seq = frobenius_trace_sequence(f, prime_bound=50)
        primes = _primes_up_to(50)
        assert len(seq) == len(primes)

    def test_s5_has_varied_patterns(self):
        """S_5 field should show multiple distinct factorization patterns."""
        f = [-1, 4, 0, -5, 0, 1]  # S_5
        data = compute_frobenius_data(f, prime_bound=200)
        patterns = set(info['pattern'] for info in data.values())
        # S_5 should have at least 3 distinct patterns
        assert len(patterns) >= 3, (
            f"S_5 field has only {len(patterns)} distinct patterns: "
            f"{patterns}")

    def test_c5_has_only_two_patterns(self):
        """C_5 field should only show (1,1,1,1,1) and (5,) patterns."""
        f = [1, 3, -3, -4, 1, 1]  # C_5
        data = compute_frobenius_data(f, prime_bound=200)
        patterns = set(info['pattern'] for info in data.values())
        for pat in patterns:
            assert pat in ((1, 1, 1, 1, 1), (5,)), (
                f"C_5 field has unexpected pattern {pat}")


# ============================================================
# Census pipeline
# ============================================================

class TestCensusPipeline:
    """Test the full census pipeline."""

    def test_census_runs(self):
        """Census completes without errors on a small prime bound."""
        results = run_full_census(prime_bound=50, verbose=False)
        assert len(results) == len(EXTENDED_TOTALLY_REAL_FIELDS)

    def test_census_finds_nonsolvable(self):
        """Census identifies multiple non-solvable cases."""
        results = run_full_census(prime_bound=100, verbose=False)
        non_solv = [r for r in results if r['solvable'] is False]
        # We have many S_5 fields in the database
        assert len(non_solv) >= 5, (
            f"Expected >= 5 non-solvable, found {len(non_solv)}")

    def test_census_palindromic_consistency(self):
        """All census entries have valid palindromic polynomials."""
        results = run_full_census(prime_bound=50, verbose=False)
        for r in results:
            assert r['is_palindromic'], (
                f"{r['label']}: palindromic check failed")

    def test_census_has_frobenius_data(self):
        """Census entries include Frobenius data."""
        results = run_full_census(prime_bound=50, verbose=False)
        for r in results:
            assert 'frobenius_data_P' in r
            assert 'frobenius_data_Q' in r
            assert 'first_20_traces' in r

    def test_census_entry_structure(self):
        """Each census entry has all expected keys."""
        expected_keys = {
            'label', 'degree', 'trace_poly', 'palindromic_poly',
            'palindromic_degree', 'is_palindromic', 'discriminant',
            'known_galois', 'detected_galois', 'solvable',
            'frobenius_data_Q', 'frobenius_data_P', 'first_20_traces',
        }
        results = run_full_census(prime_bound=50, verbose=False)
        for r in results:
            assert expected_keys.issubset(r.keys()), (
                f"{r['label']}: missing keys "
                f"{expected_keys - r.keys()}")


# ============================================================
# Non-solvable cases have degree >= 5
# ============================================================

class TestNonSolvableDegree:
    """Verify all non-solvable cases have trace field degree >= 5."""

    def test_nonsolvable_degree_at_least_5(self):
        """No field of degree < 5 should be classified as non-solvable.
        This is a theorem: S_d is solvable for d <= 4."""
        results = run_full_census(prime_bound=100, verbose=False)
        for r in results:
            if r['solvable'] is False:
                assert r['degree'] >= 5, (
                    f"{r['label']}: degree {r['degree']} marked "
                    f"non-solvable, but S_d is solvable for d<=4")

    def test_known_nonsolvable_groups_are_right(self):
        """Fields marked S_5/A_5/S_6/S_7/S_8 in the database have degree >= 5."""
        nonsolvable_groups = {'S_5', 'A_5', 'S_6', 'A_6', 'S_7', 'S_8'}
        for label, degree, poly_asc, known_gal in EXTENDED_TOTALLY_REAL_FIELDS:
            if known_gal in nonsolvable_groups:
                assert degree >= 5, (
                    f"{label}: non-solvable group {known_gal} at degree "
                    f"{degree} < 5, impossible")


# ============================================================
# Langlands test case identification
# ============================================================

class TestLanglandsTestCases:
    """Test Langlands test case identification."""

    def test_langlands_cases_exist(self):
        """At least 5 Langlands test cases should be identified."""
        results = run_full_census(prime_bound=100, verbose=False)
        cases = langlands_test_cases(results, prime_bound=100)
        assert len(cases) >= 5

    def test_langlands_cases_all_nonsolvable(self):
        """All Langlands test cases are non-solvable."""
        results = run_full_census(prime_bound=100, verbose=False)
        cases = langlands_test_cases(results, prime_bound=100)
        for case in cases:
            assert case['langlands_status'] in ('ICOSAHEDRAL', 'OPEN')

    def test_langlands_cases_have_traces(self):
        """All test cases include Frobenius trace data."""
        results = run_full_census(prime_bound=100, verbose=False)
        cases = langlands_test_cases(results, prime_bound=100)
        for case in cases:
            assert 'first_20_frobenius_traces' in case
            # Should have at least a few traces
            assert len(case['first_20_frobenius_traces']) >= 5, (
                f"{case['label']}: only "
                f"{len(case['first_20_frobenius_traces'])} traces")

    def test_langlands_artin_dimension(self):
        """Artin representation dimension is degree - 1."""
        results = run_full_census(prime_bound=100, verbose=False)
        cases = langlands_test_cases(results, prime_bound=100)
        for case in cases:
            d = case['trace_field_degree']
            assert case['artin_rep_dimension'] == d - 1

    def test_langlands_includes_s5_cases(self):
        """At least some test cases have S_5 Galois group."""
        results = run_full_census(prime_bound=100, verbose=False)
        cases = langlands_test_cases(results, prime_bound=100)
        s5_cases = [c for c in cases if 'S_5' in c['galois_group']]
        assert len(s5_cases) >= 3


# ============================================================
# Frobenius table for specific fields
# ============================================================

class TestFrobeniusTable:
    """Test detailed Frobenius table computation."""

    def test_table_for_s5_field(self):
        """Frobenius table for S_5 field disc 38569."""
        result = frobenius_table('5.5.38569.1', prime_bound=50)
        assert result['label'] == '5.5.38569.1'
        assert result['degree'] == 5
        assert len(result['table']) > 0

    def test_table_rows_structure(self):
        """Each table row has all required keys."""
        result = frobenius_table('5.5.24217.1', prime_bound=30)
        for row in result['table']:
            assert 'p' in row
            assert 'ramified' in row
            assert 'pattern_P' in row
            assert 'trace_P' in row

    def test_table_unramified_patterns_sum(self):
        """Unramified patterns sum to the correct degree."""
        result = frobenius_table('5.5.65657.1', prime_bound=100)
        for row in result['table']:
            if not row['ramified']:
                pat = row['pattern_P']
                assert sum(pat) == 5, (
                    f"p={row['p']}: pattern {pat} sums to "
                    f"{sum(pat)}, expected 5")

    def test_table_palindromic_pattern_sum(self):
        """Palindromic pattern (when unramified) sums to 2*degree."""
        result = frobenius_table('5.5.38569.1', prime_bound=50)
        for row in result['table']:
            if not row['ramified'] and row['pattern_Q'] is not None:
                pat = row['pattern_Q']
                assert sum(pat) == 10, (
                    f"p={row['p']}: palindromic pattern {pat} sums "
                    f"to {sum(pat)}, expected 10")

    def test_table_not_found_raises(self):
        """Looking up a nonexistent label raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            frobenius_table('99.99.0.0', prime_bound=30)

    def test_c5_table_only_two_patterns(self):
        """C_5 field Frobenius table shows only (1,1,1,1,1) and (5,)."""
        result = frobenius_table('5.5.14641.1', prime_bound=100)
        for row in result['table']:
            if not row['ramified']:
                assert row['pattern_P'] in ((1, 1, 1, 1, 1), (5,)), (
                    f"C_5 at p={row['p']}: unexpected pattern "
                    f"{row['pattern_P']}")


# ============================================================
# Discriminant checks
# ============================================================

class TestDiscriminants:
    """Verify discriminants of known fields."""

    def test_c5_disc_14641(self):
        """C_5 field has discriminant 11^4 = 14641."""
        f = [1, 3, -3, -4, 1, 1]
        disc = poly_discriminant(f)
        assert disc == 14641

    def test_s5_disc_38569(self):
        """S_5 field x^5-5x^3+4x-1 has disc 38569."""
        f = [-1, 4, 0, -5, 0, 1]
        disc = poly_discriminant(f)
        assert disc == 38569

    def test_s5_disc_24217(self):
        """S_5 field x^5-5x^3-x^2+3x+1 has disc 24217."""
        f = [1, 3, -1, -5, 0, 1]
        disc = poly_discriminant(f)
        assert disc == 24217

    def test_s5_disc_65657(self):
        """S_5 field x^5-x^4-5x^3+2x^2+5x+1 has disc 65657."""
        f = [1, 5, 2, -5, -1, 1]
        disc = poly_discriminant(f)
        assert disc == 65657

    def test_d5_disc_160801(self):
        """D_5 field has disc 160801 = 401^2."""
        f = [-1, 3, 4, -5, -1, 1]
        disc = poly_discriminant(f)
        assert disc == 160801
        assert is_perfect_square(disc)

    def test_c8_disc_17_pow_7(self):
        """C_8 field Q(cos(2pi/17)) has disc = 17^7 = 410338673."""
        f = [1, -4, -10, 10, 15, -6, -7, 1, 1]
        disc = poly_discriminant(f)
        assert disc == 17**7
        assert disc == 410338673

    def test_s5_disc_245_smallest(self):
        """Smallest S_5 field in database has disc 245."""
        f = [-1, 1, 4, -2, -2, 1]
        disc = poly_discriminant(f)
        assert disc == 245


# ============================================================
# Frobenius trace statistics
# ============================================================

class TestFrobeniusStatistics:
    """Test Frobenius statistics computation."""

    def test_statistics_run(self):
        """Statistics computation runs without error."""
        results = run_full_census(prime_bound=50, verbose=False)
        stats = frobenius_statistics(results, prime_bound=50)
        assert len(stats) > 0

    def test_trace_mean_near_zero_for_s5(self):
        """For S_5 fields with enough primes, the average Frobenius trace
        should be close to 0 by Chebotarev density.

        For S_5 acting on 5 letters, the average number of fixed points
        is 1 (since the average value of the permutation character is 1).
        So the average trace in the standard rep = 1 - 1 = 0.

        With 200 primes, the mean should be within ~0.5 of 0.
        """
        # Use a single well-known S_5 field for a targeted check
        entry = _compute_entry('5.5.38569.1', 5, [-1, 4, 0, -5, 0, 1],
                               'S_5', prime_bound=500)
        frob = entry['frobenius_data_P']
        traces = [v['trace'] for v in frob.values()]
        mean = sum(traces) / len(traces)
        assert abs(mean) < 0.5, (
            f"S_5 disc 38569: mean trace = {mean:.3f}, expected near 0 "
            f"(from {len(traces)} primes)")

    def test_c5_trace_stats(self):
        """C_5 field: traces are either 4 or -1, mean should be ~0."""
        results = run_full_census(prime_bound=200, verbose=False)
        stats = frobenius_statistics(results, prime_bound=200)
        c5_stats = [s for s in stats if s['label'] == '5.5.14641.1']
        assert len(c5_stats) == 1
        s = c5_stats[0]
        # For C_5, all traces are 4 (split) or -1 (inert)
        for t in s['trace_histogram'].keys():
            assert t in (4, -1), (
                f"C_5 has unexpected trace value {t}")
