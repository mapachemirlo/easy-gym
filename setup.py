# -*- coding: utf-8 -*-
import cx_Freeze

executables = [cx_Freeze.Executable("princi.py",
                                 base = "Win32GUI",
                                 icon = "Easy-gym.ico")]

build_exe_options = {"packages": [],
                     "include_files":["principal.ui", "altasocio.ui", "consulta.ui", "actualiza.ui","letra_procyon.png","logo_procyon.jpg","logo_orbis.jpg"]}

cx_Freeze.setup(
    name = "EASY GYM",
    version = "1.0.1",
    description = "Sisteme de gestión de clientes",
    options={"build_exe": build_exe_options},
    executables = executables
    )