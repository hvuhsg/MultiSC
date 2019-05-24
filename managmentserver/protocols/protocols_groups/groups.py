from .group import Group

from ..protocols_objects.user_protocol import UserProtocol
from ..protocols_objects.test_protocol import TestProtocol
from ..protocols_objects.admin_protocol import AdminProtocol
from ..protocols_objects.ms_protocol import MsProtocol
from ..protocols_objects.copmany_ms_protocol import CompanyMsProtocol
from ..protocols_objects.user_ms_protocol import UserMsProtocol
from ..protocols_objects.logs_protocol import LogsProtocol
from ..protocols_objects.user_log_protocol import UserLogsProtocol
from ..protocols_objects.company_logs_protocol import CompanyLogsProtocol
from ..protocols_objects.ml_coin_protocol import CoinProtocol
from ..protocols_objects.virtual_db_protocol import VirtualDBProtocol
from ..protocols_objects.company_protocol import CompanyProtocol

#  base group of protocols
base_group = Group("base_group", 0)
base_group.add_protocol("UserProtocol", UserProtocol())
base_group.add_protocol("CompanyProtocol", CompanyProtocol())

# protocols for test
test_group = Group("test_protocols", 2)
test_group.add_protocol("TestProtocol", TestProtocol())
test_group.add_protocol("VirtualDBProtocol", VirtualDBProtocol())

# protocols allow after login
after_user_login = Group("after_login_group", 1)
after_user_login.contain_group(base_group)
after_user_login.add_protocol("UserMsProtocol", UserMsProtocol())
after_user_login.add_protocol("UserLogsProtocol", UserLogsProtocol())
after_user_login.add_protocol("CoinProtocol", CoinProtocol())

# protocols for company's
company_options = Group("after_company_login", 1)
company_options.add_protocol("CompanyMsProtocol", CompanyMsProtocol())
company_options.add_protocol("CompanyLogsProtocol", CompanyLogsProtocol())
company_options.add_protocol("CoinProtocol", CoinProtocol())
company_options.contain_group(base_group)

# protocol for admins that allow to control
admin_options = Group("admin_options", 2)
admin_options.add_protocol("AdminProtocol", AdminProtocol())
admin_options.add_protocol("MsProtocol", MsProtocol())
admin_options.add_protocol("LogsProtocol", LogsProtocol())
admin_options.contain_group(after_user_login)
admin_options.contain_group(test_group)


all_groups = {
    "base_group": base_group,
    "after_user_login_group": after_user_login,
    "after_company_login": company_options,
    "test_group": test_group,
    "admin_options": admin_options,
}
