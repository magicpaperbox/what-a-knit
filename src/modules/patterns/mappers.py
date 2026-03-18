from flask import request

from modules.patterns.domain import Pattern, PatternCategory, Gauge, PatternDifficultyLevel


def parse_pattern_from_form() -> Pattern:
    stitches = request.form.get('gauge_stitches', type=float)
    rows = request.form.get('gauge_rows', type=float)
    if stitches is not None or rows is not None:
        target_gauge=Gauge(stitches=stitches, rows=rows)
    else:
        target_gauge = None
    difficulty_level = request.form.get('difficulty_level')
    return Pattern(
        id=None,
        name=request.form['name'],
        description=request.form['description'],
        # requirements=PatternRequirements[request.form.get('requirements')],
        target_gauge=target_gauge,
        category=PatternCategory[request.form['category']],
        subcategory=request.form.get('subcategory'),
        pattern_language=request.form.get('pattern_language'),
        author=request.form.get('author'),
        difficulty_level=PatternDifficultyLevel(difficulty_level) if difficulty_level else None,
    )