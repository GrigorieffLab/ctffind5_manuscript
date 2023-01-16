from pycistem import programs, config
from pathlib import Path

config.set_cistem_path("/home/elferich/cistem")

para = programs.apply_ctf.parameters_from_database(
    Path(__file__).parent.parent / "data/mmm/mmm/mmm.db",
    1,
    str(Path(__file__).parent.parent / "data/mmm/mmm_phaseflip.mrc")
)

para.phase_flip_only = True

programs.apply_ctf.run(para)