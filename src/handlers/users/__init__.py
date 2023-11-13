"""
Since there is only one menu, only one router was used.

However, the reaction to each button/command was placed in a
separate module for ease of writing (since some chains of
events turned out to be too long for their adequate perception
in one file).
"""
from .processing_data_from_web_app import router_for_main_menu
from .give_all_commands_bot import router_for_main_menu
from .buyer_registration import router_for_main_menu
from .start_main_menu import router_for_main_menu
from .hide_main_menu import router_for_main_menu
from .give_developer import router_for_main_menu
from .give_my_orders import router_for_main_menu
from .reviews_buyer import router_for_main_menu
from .give_manual import router_for_main_menu


__all__ = ['router_for_main_menu']
