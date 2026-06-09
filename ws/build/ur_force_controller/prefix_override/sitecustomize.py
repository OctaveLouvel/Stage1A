import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/auguste/Code/Stage/Stage_Univ_S1/ws/install/ur_force_controller'
