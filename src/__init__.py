try:
    # Python 3
    from . import energenie
    from . import cleanup_GPIO
    from . import control_any_auto
    from . import control_any_noreg
    from . import discover_mihome
    from . import Logger
    from . import mihome_energy_monitor
    from . import setup_tool
    from . import Timer
except ImportError:
    # Python 2
    import energenie
    import cleanup_GPIO
    import control_any_auto
    import control_any_noreg
    import discover_miihome
    import Logger
    import miihome_energy_monitor
    import setup_tool
    import Timer
