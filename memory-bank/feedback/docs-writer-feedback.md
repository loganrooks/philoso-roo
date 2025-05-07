# Documentation Writer Feedback Log
<!-- Add new feedback entries below this line (most recent first) -->

### [2025-05-05 14:12:11] User Intervention: CRITICAL - Invalid `.clinerules` Format (Inheritance & Headers)
- **Source**: User Input via SPARC Feedback Log [Timestamp: 2025-05-05 14:12:11 approx]
- **Document**: `docs/standards/clinerules_standard_v2.md` (and implicitly all `.clinerules` files based on it)
- **Feedback**:
    1.  **Implicit Inheritance Invalid:** `.clinerules` files MUST NOT use comments like `# --- INHERITED...`. All rules must be explicitly included.
    2.  **Token Waste:** Numbered section headers (e.g., `# 3.3 ...`) and decorative headers (`# --- ... ---`) are wasteful and MUST be removed. Only the primary YAML key is needed.
- **Analysis**: The V2.0 standard incorrectly used placeholder comments for inherited rules and included unnecessary headers, making it non-compliant with machine-readability and efficiency requirements.
- **Action**: Revised `docs/standards/clinerules_standard_v2.md` to V2.1, removing headers and explicitly including all standard rules.