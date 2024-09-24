from app.models.palette import Palette

def stylesPage():
    palette = Palette.query.filter_by(active=1).first()
    return palette