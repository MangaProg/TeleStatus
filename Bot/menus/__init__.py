# Bot/menus/__init__.py

from .admin_menus import (
    menu_admin,
    menu_admin_lojas,
    menu_admin_produtos,
    menu_admin_lojistas,
    menu_admin_relatorios,
    menu_admin_config,
)

from .user_menus import (
    menu_user,
    menu_user_produtos,
    menu_user_pontos,
)

from .shared_menus import (
    back_button,
    confirm_cancel_menu,
)