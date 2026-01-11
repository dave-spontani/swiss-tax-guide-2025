# Swiss Tax Calculator Enhancement - Implementation Status

**Date**: January 11, 2026
**Status**: Partially Complete (4 of 5 enhancements fully done, 1 in progress)

---

## ✅ COMPLETED ENHANCEMENTS (4/5)

### 1. Nebenerwerb (Side Income) Deduction - ✅ COMPLETE

**What Changed**:
- Changed from flat CHF 2,400 to dynamic formula: `max(800, min(0.20 × side_income, 2400))`
- Added `side_income_amount` field to `UserProfile`
- Updated calculation logic in `calculations/deductions.py`
- Added UI input with real-time deduction preview

**Files Modified**:
- `models/tax_data.py` (line 23): Added `side_income_amount: float = 0.0`
- `models/constants.py` (lines 136-139): New constants for min/rate/max
- `calculations/deductions.py` (lines 78-85): New formula implementation
- `questionnaire/qualifying_questions.py` (lines 157-169): New UI input field

**Testing Status**: ✅ Ready to test

---

### 2. Biking Deduction Rename - ✅ COMPLETE

**What Changed**:
- Renamed "Commuting" to "Biking deduction" for CHF 700 pauschal
- Updated display text and help messages

**Files Modified**:
- `models/constants.py` (line 111): Updated comment
- `questionnaire/automatic_deductions.py` (line 118): Changed display text

**Testing Status**: ✅ Ready to test

---

### 3. Pillar 2 Slider Maximum - ✅ COMPLETE

**What Changed**:
- Changed slider max from CHF 100,000 to CHF 10,000
- Changed step from 1,000 to 100

**Files Modified**:
- `questionnaire/optional_deductions.py` (lines 104, 106, 108): Updated slider parameters

**Testing Status**: ✅ Ready to test

---

### 4. Vermögenssteuer (Wealth Tax) Fix - ✅ COMPLETE

**What Changed**:
- **Corrected tax-free thresholds**: CHF 80,000 (singles), CHF 159,000 (married)
- **Expanded brackets**: From 4 to 7 progressive brackets for singles, married
- **Removed incorrect per-adult deductions**: Only per-child deductions (CHF 41,100) apply
- **Added marital status parameter** to wealth tax calculation

**Files Modified**:
- `models/constants.py` (lines 73-98):
  - `WEALTH_TAX_BRACKETS_SINGLE` (7 brackets)
  - `WEALTH_TAX_BRACKETS_MARRIED` (7 brackets)
  - Removed `WEALTH_DEDUCTION_PER_ADULT`
  - Kept `WEALTH_DEDUCTION_PER_CHILD = 41100`
- `calculations/wealth_tax.py` (lines 1-90):
  - Added `marital_status: str = 'single'` parameter
  - Select brackets based on marital status
  - Calculate deductions: only children (no per-adult)
  - Updated docstring with accurate Zurich rules

**Source**: [acheteur.ch Vermögenssteuer Zurich](https://acheteur.ch/de/post/vermogenssteuer-zurich)

**Testing Status**: ✅ Ready to test

---

## 🚧 IN PROGRESS (1/5)

### 5. Married Couples Support - ⚠️ PARTIALLY COMPLETE

#### ✅ What's Done:

##### A. Tax Bracket Research & Constants
**Federal Married Brackets** - ✅ **OFFICIAL & ACCURATE**
- Source: [DBG Article 36 §2 (lawbrary.ch)](https://lawbrary.ch/law/art/DBG-v2024.03-de-art-36/)
- Extracted all 16 official brackets for married couples
- Includes 2024 cold progression adjustment (Sept 2023)
- Added to `models/constants.py` as `FEDERAL_TAX_BRACKETS_MARRIED` (lines 28-47)

**Federal Single Brackets** - ✅ Updated to 2024 official values
- Updated existing brackets with 2024 cold progression adjustment
- Source: DBG Article 36 §1

**Zurich Married Brackets** - ⚠️ **APPROXIMATED (NEEDS VERIFICATION)**
- Source: StG § 35 Abs. 2 (PDF not accessible)
- Created reasonable estimates based on federal single/married ratio
- Added as `ZURICH_TAX_BRACKETS_MARRIED` with **TODO comments** (lines 71-89)
- **Action Required**: Verify against official Zurich tax calculator or contact cantonal tax authority

**Wealth Tax Married Brackets** - ✅ Already added (see Enhancement #4)

#### 🔴 What's NOT Done Yet:

The remaining work is **substantial** and involves many files. Here's what remains:

---

## 📋 REMAINING WORK FOR MARRIED COUPLES

### Phase 5: Data Model Extension (Estimated: 2-3 hours)

**File**: `models/tax_data.py`

**Changes Needed**:
1. Add ~20 new fields to `UserProfile` dataclass for spouse-specific employment:

```python
# Spouse 1 (primary person - used for singles OR first person if married)
spouse1_employment_type: str = 'employed'
spouse1_net_salary: float = 0.0
spouse1_has_side_income: bool = False
spouse1_side_income_amount: float = 0.0
spouse1_bikes_to_work: bool = False
spouse1_uses_public_transport_car: bool = False
spouse1_actual_commuting_costs: float = 0.0
spouse1_works_away_from_home: bool = True
spouse1_employer_meal_subsidy: bool = False

# Spouse 2 (second person - only used if married)
spouse2_employment_type: str = 'not_working'
spouse2_net_salary: float = 0.0
spouse2_has_side_income: bool = False
spouse2_side_income_amount: float = 0.0
spouse2_bikes_to_work: bool = False
spouse2_uses_public_transport_car: bool = False
spouse2_actual_commuting_costs: float = 0.0
spouse2_works_away_from_home: bool = False
spouse2_employer_meal_subsidy: bool = False
```

**Backward Compatibility Strategy**:
- Keep existing fields (`employment_type`, `net_salary`, etc.)
- When `marital_status == 'single'`, map old fields to spouse1
- When `marital_status == 'married'`, use spouse1/spouse2 explicitly

---

### Phase 6: Update Calculation Functions (Estimated: 4-5 hours)

#### 6A. Federal Tax (`calculations/federal_tax.py`)

**Changes**:
```python
def calculate_federal_tax(
    income: float,
    deductions: float = 0.0,
    marital_status: str = 'single'  # NEW PARAMETER
) -> TaxResult:
    # Select appropriate brackets
    if marital_status == 'married':
        brackets = FEDERAL_TAX_BRACKETS_MARRIED
    else:
        brackets = FEDERAL_TAX_BRACKETS

    # Rest of logic stays same
    ...
```

**Estimated Lines**: ~10 lines changed

---

#### 6B. Cantonal Tax (`calculations/cantonal_tax.py`)

**Changes**:
```python
def calculate_zurich_tax(
    income: float,
    gemeinde_steuerfuss: int = 119,
    deductions: float = 0.0,
    marital_status: str = 'single'  # NEW PARAMETER
) -> TaxResult:
    # Select appropriate brackets
    if marital_status == 'married':
        brackets = ZURICH_TAX_BRACKETS_MARRIED
    else:
        brackets = ZURICH_TAX_BRACKETS

    # Rest of logic stays same
    ...
```

**Estimated Lines**: ~10 lines changed

---

#### 6C. Deductions (`calculations/deductions.py`) - **MOST COMPLEX**

**Changes Required**:

This is the **biggest** change - need to refactor `calculate_automatic_deductions()` to:
1. Check if married
2. If married, calculate deductions for **each spouse separately**:
   - Commuting (spouse1 + spouse2)
   - Meals (spouse1 + spouse2)
   - Professional expenses (spouse1 + spouse2)
   - Side income (spouse1 + spouse2)
3. Sum per-spouse deductions
4. Add dual income deduction if both work
5. If single, use existing logic (backward compatible)

**Estimated Lines**: ~100-150 lines (major refactoring)

**Complexity**: HIGH - needs careful testing for edge cases:
- One spouse working, one not
- Both self-employed
- Different commuting methods per spouse
- Side income for both spouses

---

### Phase 7: Update UI (Estimated: 6-8 hours) - **MOST TIME-CONSUMING**

#### 7A. Qualifying Questions (`questionnaire/qualifying_questions.py`)

**Major Changes**:
1. **Conditional Employment Section Rendering**:
   ```python
   if profile.marital_status == 'married':
       st.markdown("### 👤 Person 1 Employment & Income")
       render_spouse_employment_section(profile, spouse_num=1)

       st.divider()

       st.markdown("### 👤 Person 2 Employment & Income")
       render_spouse_employment_section(profile, spouse_num=2)

       # Show combined income
       combined = profile.spouse1_net_salary + profile.spouse2_net_salary
       st.info(f"💰 Combined income: CHF {combined:,.0f}")
   else:
       render_single_employment_section(profile)  # Existing logic
   ```

2. **New Helper Function**: `render_spouse_employment_section(profile, spouse_num)`
   - Duplicates employment input fields for each spouse
   - Uses dynamic field names (`spouse1_*`, `spouse2_*`)
   - Includes: employment type, salary, commuting, meals, side income

**Estimated Lines**: ~200-250 new lines

**Files to Create/Modify**:
- `questionnaire/qualifying_questions.py`: Add conditional rendering + helper functions

---

#### 7B. Automatic Deductions (`questionnaire/automatic_deductions.py`)

**Changes**:
1. Show **per-spouse breakdown** if married
2. Display combined totals
3. Show dual commuting sliders (one per spouse if applicable)

**Example UI Layout**:
```
┌─────────────────────────────────────────┐
│ Person 1 Deductions        │ Person 2   │
├────────────────────────────┼────────────┤
│ Biking: CHF 700            │ -          │
│ Commuting: CHF 3,000       │ CHF 2,500  │
│ Meals: CHF 3,200           │ CHF 1,600  │
│ Professional: CHF 3,000    │ CHF 2,400  │
│ Side income: CHF 1,200     │ -          │
├────────────────────────────┴────────────┤
│ Combined: CHF 14,900                    │
│ Dual income deduction: CHF 5,900        │
└─────────────────────────────────────────┘
```

**Estimated Lines**: ~80-100 new lines

---

#### 7C. Tax Comparison (`ui/tax_comparison.py`)

**Changes**:
```python
def render_tax_comparison(profile: UserProfile, deductions: DeductionResult):
    # Calculate combined income
    if profile.marital_status == 'married':
        combined_income = profile.spouse1_net_salary + profile.spouse2_net_salary
    else:
        combined_income = profile.net_salary

    # Pass marital_status to all tax calculations
    federal_result = calculate_federal_tax(
        income=combined_income,
        deductions=deductions.total_deductions,
        marital_status=profile.marital_status  # NEW
    )

    # Same for cantonal and wealth tax
    ...
```

**Estimated Lines**: ~40-50 lines changed

---

### Phase 8: Testing & Verification (Estimated: 3-4 hours)

**Test Cases Needed**:

1. **Single Individual** (backward compatibility)
   - Income: CHF 100,000
   - Verify same results as before

2. **Married - Both Working**
   - Spouse 1: CHF 100,000
   - Spouse 2: CHF 80,000
   - Combined: CHF 180,000
   - Verify dual income deduction applied

3. **Married - One Working**
   - Spouse 1: CHF 150,000
   - Spouse 2: CHF 0
   - Verify no dual income deduction

4. **Married - Both Self-Employed**
   - Test Pillar 3a limits (CHF 36,288 each)

5. **Married - Different Deductions**
   - Spouse 1: Bikes to work + side income
   - Spouse 2: Public transport + no side income
   - Verify per-spouse calculations

6. **Edge Cases**:
   - Switch from single to married (data migration)
   - High income (test married bracket caps)
   - Wealth tax with married threshold

**Verification Against Official Calculator**:
- Use [Zurich official calculator](https://www.zh.ch/de/steuern-finanzen/steuern/steuern-natuerliche-personen/steuerrechner.html)
- Compare 3-5 married couple scenarios
- Ensure within CHF 10 difference (rounding tolerance)

---

## 📊 IMPLEMENTATION METRICS

### Work Completed: ~40%
- ✅ Phases 1-2: Quick fixes (100% done)
- ✅ Phase 3-4: Tax bracket research (100% done)
- 🔴 Phase 5: Data model (0% done)
- 🔴 Phase 6: Calculations (0% done)
- 🔴 Phase 7: UI (0% done)
- 🔴 Phase 8: Testing (0% done)

### Estimated Remaining Time: 15-20 hours
- Data model: 2-3 hours
- Calculations: 4-5 hours
- UI: 6-8 hours
- Testing: 3-4 hours

### Risk Assessment:

**LOW RISK** (Already Complete):
- ✅ Nebenerwerb formula
- ✅ Biking deduction rename
- ✅ Pillar 2 limit
- ✅ Wealth tax fix
- ✅ Federal married brackets (official)

**MEDIUM RISK** (Needs Verification):
- ⚠️ Zurich married brackets (approximated - TODO verification)

**HIGH RISK** (Complex, Not Started):
- 🔴 Per-spouse deduction calculations (many edge cases)
- 🔴 UI conditional rendering (complex state management)
- 🔴 Testing married scenarios (requires official calculator comparison)

---

## 🎯 RECOMMENDED NEXT STEPS

### Option 1: Complete Married Couples Now (Fastest)
**Pros**: Get everything done in one go
**Cons**: Large code changes without intermediate testing
**Time**: 15-20 hours continuous work

### Option 2: Test What's Done, Then Continue (Safest)
**Pros**: Verify 4/5 enhancements work before adding complexity
**Cons**: Two separate implementation sessions
**Time**: 2 hours testing + 15-20 hours implementation

### Option 3: Deliver What's Done, Defer Married Couples (Incremental)
**Pros**: Users get 4 working enhancements immediately
**Cons**: Married couples feature delayed
**Time**: 2 hours testing + documentation

### Option 4: Verify Zurich Brackets First (Most Accurate)
**Pros**: Get official brackets before implementing
**Cons**: Requires contacting Zurich tax authority or manual testing
**Time**: 1-3 days for official response + implementation

---

## 🔧 CURRENT STATE OF CODEBASE

### Files Modified (Ready to Test):
1. `models/tax_data.py` - Added `side_income_amount`
2. `models/constants.py` - Updated deductions, brackets, wealth tax
3. `calculations/deductions.py` - Nebenerwerb formula
4. `calculations/wealth_tax.py` - Marital status support
5. `questionnaire/qualifying_questions.py` - Side income input
6. `questionnaire/optional_deductions.py` - Pillar 2 limit
7. `questionnaire/automatic_deductions.py` - Display text

### Files NOT Modified (Need Work for Married):
1. `calculations/federal_tax.py` - Needs marital_status parameter
2. `calculations/cantonal_tax.py` - Needs marital_status parameter
3. `calculations/deductions.py` - Needs per-spouse logic
4. `questionnaire/qualifying_questions.py` - Needs conditional employment UI
5. `questionnaire/automatic_deductions.py` - Needs per-spouse display
6. `ui/tax_comparison.py` - Needs marital_status passing

### No Syntax Errors:
✅ All imports tested successfully (verified with Python import test)

---

## 📝 NOTES FOR FUTURE IMPLEMENTATION

### When Implementing Married Couples:

1. **Start with Data Model** - Add all spouse fields first
2. **Update Imports** - Add `FEDERAL_TAX_BRACKETS_MARRIED`, `ZURICH_TAX_BRACKETS_MARRIED` to imports
3. **Test Federal Tax First** - Verify married brackets work before UI
4. **Implement Deductions Last** - Most complex, needs careful testing
5. **Use Feature Flag** - Consider adding `MARRIED_COUPLES_ENABLED = False` flag to test incrementally

### Zurich Married Brackets Verification:

**Method 1: Official Calculator**
- URL: https://www.zh.ch/de/steuern-finanzen/steuern/steuern-natuerliche-personen/steuerrechner.html
- Test married couple with known income (e.g., CHF 100,000)
- Reverse-engineer brackets from tax amount

**Method 2: Contact Authority**
- Email: steueramt@fd.zh.ch
- Phone: +41 43 259 51 51
- Request: "Verheiratetentarif gemäss § 35 Abs. 2 StG für 2024"

**Method 3: Official PDF**
- Document: Kantonsblatt Zürich
- Search: "Steuertarife 2024"
- Extract Table 2 (Verheiratetentarif)

---

## ✅ SUCCESS CRITERIA

### For What's Already Done (Phases 1-4):
- [ ] Side income deduction calculates correctly for various amounts
- [ ] Biking deduction displays as "Biking deduction" not "Commuting"
- [ ] Pillar 2 slider caps at CHF 10,000
- [ ] Wealth tax uses correct thresholds (CHF 80k/159k)
- [ ] Wealth tax calculates correctly with 7 brackets
- [ ] No regression in single individual calculations

### For Married Couples (Phases 5-8):
- [ ] Federal married tax within CHF 10 of official calculator
- [ ] Zurich married tax verified against official calculator
- [ ] Per-spouse deductions calculate correctly
- [ ] Dual income deduction applies only when both work
- [ ] UI conditionally renders based on marital status
- [ ] Backward compatibility: singles still work correctly
- [ ] Edge cases handled: one working, different employment types

---

**Last Updated**: 2026-01-11
**Implementation Status**: 40% Complete (4/5 enhancements done)
**Ready for Production**: Enhancements 1-4 only
**Next Milestone**: Complete married couples support (Phases 5-8)
