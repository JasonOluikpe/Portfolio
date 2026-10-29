from .config import STATIC_URL
from .models import ClipData, Project

PROFILE = dict(
    name='Jason Oluikpe',
    role='Future SWE',
    tagline='4th year Computer Science Student looking for an ==*internship*==.',
    linkedin='https://www.linkedin.com/in/ebubeoluikpe/',
    resume=f'{STATIC_URL}/Resume.pdf',
    email='oluikpe.ebube@gmail.com',
)

PROJECT = Project(
    name='Better IDE',
    summary='A lightweight python IDE coded from ***scratch***.',
    description=(
        'While pursing my degree, I have been developing this personal project and applying '
        'the concepts and coding principles covered in my classes.'
    ),
    stack=['Python', 'Code Modularity', 'Object-Oriented Programming', 'Better than IDLE'],
    links=[
        ('icon:apple', 'https://github.com/JasonOluikpe/Portfolio/releases/download/v1.4.1/BetterIDE-1.4.1.dmg'),
        ('icon:windows', ''),
    ],
    overview=('media/overview.mp4', 'Insert Video Here'),
    clips=[
        ('Split Screen Editing', 'Working with two files at the ***same time***. Easy swapping with `Ctrl+1` and `Ctrl+2`.', 'media/split.mp4'),
        ('Close/Re-open Tabs', 'Closing tabs with `Ctrl+W` and re-opening them with `Ctrl+Shift+T`.', 'media/close.mp4'),
        ('Autosave', "Don't have to worry about saving files anymore, it saves on ***idle*** and when file is closed.", 'media/save.mp4'),
        ('Workspace', 'Use `Ctrl+K` to open a folder and `Ctrl+E` to toggle the workspace.', 'media/workspace.mp4'),
        ('Open File', 'Open files with/without a workspace with `Ctrl+O` for quick and simple editing.', 'media/open.mp4'),
        ('Move Lines', 'Move ***lines*** of code with `Alt+Up` or `Alt+Down`. On MacOS, use `Option+Up` or `Option+Down`', 'media/move.mp4'),
    ],
    more='Still not impressed?',
    joke='Did I mention I built these ==***FROM SCRATCH***==',
    more_clips=[
        ('Run Code', 'Run whatever file you are working on with `Ctrl+Enter`. Toggle the terminal with `Ctrl+T`.', 'media/run.mp4'),
        ('Multi-line Cursor', 'Can code on more than one line at a time, even in different positions.', 'media/multi.mp4'),
        ('Individual Find', 'Each tab has its own find, use with `Ctrl+F`', 'media/find.mp4'),
        ('Built-In Terminal', 'Working terminal used for all sorts of things like installing packages and recieving output.', 'media/terminal.mp4'),
        ('Syntax Checker', 'A built-in syntax checker for causal mistakes.', 'media/syntax.mp4'),
        ('Automatic VENV', 'If no virtual environment is detected, it builds one in the same location as file.', 'media/venv.mp4'),
    ],
)

ABOUT = [
    (
        "I’m currently studying at **Brock University** and looking for an "
        "==**internship**==. I see myself as ==*more than a programmer*.== "
        "I balance work, school, gym, personal projects, and my really hot girlfriend "
        "(hardest part). I bring **high energy** into ==*everything*== I do, especially my work. "
        "I work part-time at **Aerosports Trampoline Park** in St. Catharines where "
        "I've built a strong record of positive feedback and customer satisfaction!"
    ),
]

ABOUT_CLIPS: list[ClipData] = [  # Title, Caption, Filepath
    ('Gym Session', "Been working out for about 4 years.", 'media/gym.mp4'),
    ('Date Night', "Braided my girlfriend's hair before we went bowling.", 'media/gf.mp4'),
    ('My Dog', 'Her name is waffles!', 'media/dog.mp4'),
]

FEATURABLE_WIDGET_ID = 'c97dee88-e824-4a2c-994f-42b3e6e427df'

REFERENCES: list[tuple[str, str, str]] = [  # Name, Job title, Phone
    ('Gareth', 'Aerosports Supervisor', '+1 (365) 855-2719'),
    ('Dupinder Kaur', 'Aerosports Manager', '+1 (289) 697-7882'),
]