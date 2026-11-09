from .models import ClipData, Project

PROFILE = dict(
    name='Jason Oluikpe',
    role='Future SWE',
    tagline='4th year Computer Science Student looking for an ==*internship*==.',
    linkedin='https://www.linkedin.com/in/ebubeoluikpe/',
    github='https://github.com/JasonOluikpe',
    resume='https://jasonoluikpe.github.io/Portfolio-Media/Resume.pdf',
    email='oluikpe.ebube@gmail.com',
    logo='https://jasonoluikpe.github.io/Portfolio-Media/logo.png',
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
        ('icon:apple', ''),
        ('icon:windows', ''),
    ],
    overview='https://jasonoluikpe.github.io/Portfolio-Media/overview.mp4',
    clips=[
        ('Split Screen Editing', 'Working with two files at the ***same time***. Easy swapping with `Ctrl+1` and `Ctrl+2`.', 'https://jasonoluikpe.github.io/Portfolio-Media/split.mp4'),
        ('Close/Re-open Tabs', 'Closing tabs with `Ctrl+W` and re-opening them with `Ctrl+Shift+T`.', 'https://jasonoluikpe.github.io/Portfolio-Media/close.mp4'),
        ('Autosave', "Don't have to worry about saving files anymore, it saves on ***idle*** and when file is closed.", 'https://jasonoluikpe.github.io/Portfolio-Media/save.mp4'),
        ('Workspace', 'Use `Ctrl+K` to open a folder and `Ctrl+E` to toggle the workspace.', 'https://jasonoluikpe.github.io/Portfolio-Media/workspace.mp4'),
        ('Open File', 'Open files with/without a workspace with `Ctrl+O` for quick and simple editing.', 'https://jasonoluikpe.github.io/Portfolio-Media/open.mp4'),
        ('Move Lines', 'Move ***lines*** of code with `Alt+Up` or `Alt+Down`. On MacOS, use `Option+Up` or `Option+Down`', 'https://jasonoluikpe.github.io/Portfolio-Media/move.mp4'),
    ],
    more='Still not impressed?',
    joke='Did I mention I built these ==***FROM SCRATCH***==',
    more_clips=[
        ('Run Code', 'Run whatever file you are working on with `Ctrl+Enter`. Toggle the terminal with `Ctrl+T`.', 'https://jasonoluikpe.github.io/Portfolio-Media/run.mp4'),
        ('Multi-line Cursor', 'Can code on more than one line at a time, even in different positions.', 'https://jasonoluikpe.github.io/Portfolio-Media/multi.mp4'),
        ('Individual Find', 'Each tab has its own find, use with `Ctrl+F`', 'https://jasonoluikpe.github.io/Portfolio-Media/find.mp4'),
        ('Built-In Terminal', 'Working terminal used for all sorts of things like installing packages and recieving output.', 'https://jasonoluikpe.github.io/Portfolio-Media/terminal.mp4'),
        ('Syntax Checker', 'A built-in syntax checker for causal mistakes.', 'https://jasonoluikpe.github.io/Portfolio-Media/syntax.mp4'),
        ('Automatic VENV', 'If no virtual environment is detected, it builds one in the same location as file.', 'https://jasonoluikpe.github.io/Portfolio-Media/venv.mp4'),
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

ABOUT_CLIPS: list[ClipData] = [
    ('Gym Session', "Been working out for about 4 years.", 'https://jasonoluikpe.github.io/Portfolio-Media/gym.mp4'),
    ('Date Night', "Braided my girlfriend's hair before we went bowling.", 'https://jasonoluikpe.github.io/Portfolio-Media/gf.mp4'),
    ('My Dog', 'Her name is waffles!', 'https://jasonoluikpe.github.io/Portfolio-Media/dog.mp4'),
]

FEATURABLE_WIDGET_ID = 'c97dee88-e824-4a2c-994f-42b3e6e427df'

REFERENCES: list[tuple[str, str, str]] = [  # Name, Job title, Phone
    ('Gareth', 'Aerosports Supervisor', '+1 (365) 855-2719'),
    ('Dupinder Kaur', 'Aerosports Manager', '+1 (289) 697-7882'),
]