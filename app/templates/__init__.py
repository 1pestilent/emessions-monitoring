from fastapi.templating import Jinja2Templates

from app.core.config import TEMPLATE_DIR

template = Jinja2Templates(directory=TEMPLATE_DIR)