"""Static teaching content for Titan Robotics.

Short, plain-English explainers. No jargon, no war framing, no external links.
"""

from __future__ import annotations

#: The three pillars of robotics, used on the Home page.
PILLARS = (
    {
        "emoji": "👁️",
        "name": "Sense",
        "question": "What is going on out there?",
        "text": "Cameras, distance sensors, microphones and motion sensors turn the physical world into numbers a computer can read.",
        "extra": "👁️ Camera · 📡 Radar · 🎤 Microphone · 🧭 Gyroscope",
    },
    {
        "emoji": "🧠",
        "name": "Think",
        "question": "What should I do next?",
        "text": "The processor runs the robot's plan: it filters noisy sensor data, builds a map, and picks the next safe action.",
        "extra": "🧩 Filter · 🗺️ Map · 🧮 Plan · ✅ Check",
    },
    {
        "emoji": "💪",
        "name": "Act",
        "question": "How do I move the world?",
        "text": "Motors, joints, wheels, propellers and lights carry out the decision, then sensors report back on what actually happened.",
        "extra": "⚙️ Motor · 🦿 Joint · 🛞 Wheel · 🚁 Rotor",
    },
)

#: The four building blocks explained on the How Robots Work page.
ROBOT_PARTS = (
    {
        "emoji": "👁️",
        "name": "Sensors",
        "subtitle": "The robot's senses",
        "text": "A sensor is any part that turns the real world into a signal: light, distance, sound, heat, tilt or pressure. "
        "Sensors are never perfect, so engineers often use several kinds together - a camera plus a distance sensor - because two different views are much harder to fool than one.",
        "examples": "📷 camera · 📡 lidar & radar · 🎤 microphone · 🧭 gyroscope · 🌡️ thermometer · 🛰️ GPS receiver",
        "diagram": [("📷", "Camera"), ("📡", "Lidar"), ("🎤", "Sound"), ("🧭", "Tilt"), ("🌡️", "Heat")],
        "caption": "Many senses, one picture of the world.",
    },
    {
        "emoji": "💪",
        "name": "Actuators",
        "subtitle": "The robot's muscles",
        "text": "An actuator is the part that moves something, usually by turning electricity into motion. A motor spins a wheel, a servo angles a joint, a gripper closes around an object, and a speaker makes sound. "
        "If sensors are the robot's eyes, actuators are its hands and feet.",
        "examples": "⚙️ electric motors · 🦿 servo joints · 🦾 grippers · 🚁 propellers · 🧲 electromagnets · 🔊 speakers",
        "diagram": [("⚡", "Signal"), ("🔄", "Motor"), ("🦿", "Joint"), ("🦾", "Grip"), ("🚗", "Wheel")],
        "caption": "Energy in, movement out.",
    },
    {
        "emoji": "🧠",
        "name": "Processor",
        "subtitle": "The robot's brain",
        "text": "The processor is a small computer that decides what the robot should do. It reads the sensor signals, cleans out the noise, builds a map of the surroundings and chooses the next action - often many times every second. "
        "Most robots keep a human supervisor in the loop for big decisions.",
        "examples": "🧠 CPUs and GPUs · 🧩 sensor fusion · 🗺️ mapping · 🧮 path planning · 🛡️ safety limits",
        "diagram": [("🎤", "Input"), ("🧠", "Chip"), ("🧮", "Plan"), ("📶", "Command")],
        "caption": "Decisions faster than a human blink.",
    },
    {
        "emoji": "🔋",
        "name": "Power",
        "subtitle": "The robot's food",
        "text": "Robots need energy to move and think. Batteries are light and quiet but run down; a cable gives steady power but ties the robot to one place; solar panels are clean but slow. "
        "Engineers trade these off, because every kilogram of battery is a kilogram the robot cannot use for tools.",
        "examples": "🔋 lithium batteries · 🔌 tethered cable · ☀️ solar panels · 🔥 fuel cells · ♻️ braking regeneration",
        "diagram": [("🔋", "Battery"), ("🔌", "Regulator"), ("⚙️", "Motors"), ("📊", "Monitor"), ("♻️", "Recharge")],
        "caption": "Energy budget, checked constantly.",
    },
)

#: Robot latency presets for the reaction-distance playground.
LATENCY_PRESETS = (
    ("🏭 Warehouse robot taking a shelf to a picker", 2.0, 60),
    ("📦 Sidewalk delivery robot", 1.5, 90),
    ("🐕 Four-legged inspection robot, walking", 1.6, 120),
    ("🐎 Four-legged inspection robot, running", 3.0, 120),
    ("🛣️ Highway inspection drone", 25.0, 80),
)

#: Quick glossary shown in an expander.
GLOSSARY = (
    ("Sensor", "A part that measures the real world: light, distance, sound, heat, tilt or pressure."),
    ("Actuator", "A part that creates movement, such as a motor, servo joint or gripper."),
    ("Lidar", "A sensor that measures distance by timing a laser pulse as it bounces back."),
    ("Latency", "The delay between something happening and the robot reacting to it."),
    ("Sensor fusion", "Combining several sensors so mistakes in one are corrected by the others."),
    ("Teleoperation", "A human drives the robot from a control station; this is how most field robots work."),
    ("Autonomy level", "How much a robot decides on its own, from 'human does everything' to 'robot does everything'."),
    ("SLAM", "Building a map and tracking your own position on it at the same time."),
)

#: Rules-of-thumb shown on the How Robots Work page.
SAFETY_RULES = (
    ("☂️ Fail safe", "If the robot loses its link or its battery gets low, it slows down and stops somewhere safe."),
    ("🧑‍✈️ Human in charge", "A trained operator can always take over, and keeps responsibility for what the robot does."),
    ("🔍 Explain the decision", "Good robots can say why they stopped or slowed, which makes problems easy to find."),
    ("🙈 Privacy by design", "Data is used only for the task at hand, deleted when it is no longer needed and never sold."),
)

#: Balanced counterpoints listed on the Future page.
FUTURE_CHALLENGES = (
    ("🔐 Safety", "A robot that can lift a box can also drop it. Testing and certification must grow as fast as the abilities do."),
    ("🛡️ Privacy", "Cameras and microphones on wheels need clear rules about what is recorded, how long it is kept and who can see it."),
    ("💼 Work", "Automation moves tasks rather than whole jobs in most cases, but retraining people has to be planned, not left to chance."),
    ("🌍 Energy & materials", "Every robot has an environmental bill. Repairable design and recycling of batteries and motors matter as much as the software."),
    ("⚖️ Fair access", "If helpful robots are only affordable to a few, the gap grows. Libraries, schools and clinics are good first places for them."),
)

#: Prompt cards for the "sketch your own robot" activity.
SKETCH_PROMPTS = (
    "What job will it do, and who does that job today?",
    "What will it sense, and what happens when a sensor is wrong?",
    "What is its weakness, and how does it fail safely?",
    "How will it get energy and stay within its power budget?",
    "Who is responsible when it makes a mistake?",
)
