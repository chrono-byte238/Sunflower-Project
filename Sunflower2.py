import argparse
import hashlib
import math
import textwrap
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageTk


WIDTH = 900
HEIGHT = 900
FLOWER_X = 0
FLOWER_Y = 100
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))
BACKGROUND = "#101b22"
ANIMATION_FILE = Path(__file__).with_name("Sunflower_animation.gif")
DEFAULT_MESSAGE = "Hello world"


def image_point(point):
    x, y = point
    return (WIDTH / 2 + x, HEIGHT / 2 - y)


def add_frame(frames, canvas, duration=70):
    frames.append(canvas.quantize(colors=256, method=Image.Quantize.FASTOCTREE))
    return duration


def leaf_points(start, angle_degrees, length=150, width=48):
    angle = math.radians(angle_degrees)
    along = (math.cos(angle), math.sin(angle))
    across = (-math.sin(angle), math.cos(angle))
    points = []
    for side in (1, -1):
        steps = range(21) if side == 1 else range(20, -1, -1)
        for step in steps:
            t = step / 20
            half_width = width * math.sin(math.pi * t) ** 0.8
            x = start[0] + along[0] * length * t + across[0] * half_width * side
            y = start[1] + along[1] * length * t + across[1] * half_width * side
            points.append((x, y))
    return points


def draw_animation(message=DEFAULT_MESSAGE):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    frames = []
    durations = []

    stem_points = []
    for step in range(41):
        t = step / 40
        x = 26 * math.sin(t * math.pi * 0.75)
        y = FLOWER_Y - 15 - 390 * t
        stem_points.append(image_point((x, y)))
        if step > 0:
            draw.line(stem_points[-2:], fill="#286b35", width=18)
        if step and step % 3 == 0:
            durations.append(add_frame(frames, canvas, 45))

    leaf_specs = [
        (-4, FLOWER_Y - 145, 150, 155),
        (15, FLOWER_Y - 250, 145, 25),
    ]
    for stem_x, stem_y, length, angle in leaf_specs:
        start = (stem_x, stem_y)
        end_angle = math.radians(angle)
        end = (
            stem_x + length * math.cos(end_angle),
            stem_y + length * math.sin(end_angle),
        )
        points = [image_point(point) for point in leaf_points(start, angle, length)]
        draw.polygon(points, fill="#368a45")
        draw.line(
            (image_point(start), image_point(end)),
            fill="#236536",
            width=2,
        )
        durations.append(add_frame(frames, canvas, 100))

    petal_colors = ("#ffc928", "#ffb91f", "#ffda45")
    petal_count = 34
    for index in range(petal_count):
        angle = 2 * math.pi * index / petal_count
        direction = (math.cos(angle), math.sin(angle))
        across = (-direction[1], direction[0])
        base_x = FLOWER_X + direction[0] * 44
        base_y = FLOWER_Y + direction[1] * 44
        points = []
        for side in (1, -1):
            steps = range(25) if side == 1 else range(24, -1, -1)
            for step in steps:
                t = step / 24
                half_width = 28 * math.sin(math.pi * t) ** 0.75
                x = base_x + direction[0] * 178 * t + across[0] * half_width * side
                y = base_y + direction[1] * 178 * t + across[1] * half_width * side
                points.append(image_point((x, y)))
        draw.polygon(points, fill=petal_colors[index % len(petal_colors)])
        durations.append(add_frame(frames, canvas, 55))

    center = image_point((FLOWER_X, FLOWER_Y))
    radius = 150
    cx, cy = center
    draw.ellipse(
        (cx - radius - 3, cy - radius - 3, cx + radius + 3, cy + radius + 3),
        fill="#633713",
    )
    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill="#75451e",
    )

    seed_colors = ("#302319", "#49301c", "#9a682e", "#c08a3d")
    for index in range(1, 1400):
        angle = index * GOLDEN_ANGLE
        distance = 3.9 * math.sqrt(index)
        point = image_point(
            (
                FLOWER_X + distance * math.cos(angle),
                FLOWER_Y + distance * math.sin(angle),
            )
        )
        x, y = point
        color = seed_colors[index % len(seed_colors)]
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=color)
        if index % 35 == 0:
            durations.append(add_frame(frames, canvas, 45))

    heart_points = []
    for step in range(121):
        angle = 2 * math.pi * step / 120
        x = FLOWER_X + 5.3 * 16 * math.sin(angle) ** 3
        y = FLOWER_Y + 4.5 * (
            13 * math.cos(angle)
            - 5 * math.cos(2 * angle)
            - 2 * math.cos(3 * angle)
            - math.cos(4 * angle)
        )
        heart_points.append(image_point((x, y)))
    draw.polygon(heart_points, fill="#b8324b")
    durations.append(add_frame(frames, canvas, 120))

    message_lines = textwrap.wrap(message, width=20) or [""]
    message_text = "\n".join(message_lines)
    for font_size in range(16, 7, -1):
        try:
            message_font = ImageFont.truetype("arialbd.ttf", font_size)
        except OSError:
            message_font = ImageFont.load_default(size=font_size)
        left, top, right, bottom = draw.multiline_textbbox(
            (0, 0), message_text, font=message_font, spacing=2, align="center"
        )
        if right - left <= 220 and bottom - top <= 130:
            break
    else:
        raise ValueError("Le message est trop long pour tenir dans le cœur.")

    draw.multiline_text(
        image_point((FLOWER_X, FLOWER_Y)),
        message_text,
        fill="#fff4d6",
        font=message_font,
        spacing=2,
        align="center",
        anchor="mm",
    )
    durations.append(add_frame(frames, canvas, 1400))
    return frames, durations


def save_animation(path, message=DEFAULT_MESSAGE):
    frames, durations = draw_animation(message)
    temporary_path = path.with_name(path.stem + ".tmp.gif")
    try:
        frames[0].save(
            temporary_path,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            disposal=2,
            optimize=False,
        )
        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def play_animation(path):
    root = tk.Tk()
    root.title("Sunflower Animation")
    root.resizable(False, False)

    with Image.open(path) as animation:
        label = tk.Label(root, bg=BACKGROUND, borderwidth=0)
        label.pack()
        frame_count = animation.n_frames

        def show_frame(index):
            animation.seek(index)
            frame = ImageTk.PhotoImage(animation.convert("RGB"), master=root)
            label.configure(image=frame)
            label.image = frame
            delay = animation.info.get("duration", 70)
            root.after(max(20, delay), show_frame, (index + 1) % frame_count)

        show_frame(0)
        root.mainloop()


def animation_path(message):
    if message == DEFAULT_MESSAGE:
        return ANIMATION_FILE

    message_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()[:12]
    return ANIMATION_FILE.with_name(
        f"{ANIMATION_FILE.stem}-{message_hash}{ANIMATION_FILE.suffix}"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Play the saved sunflower animation.")
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="create a fresh animation and replace the saved GIF",
    )
    parser.add_argument(
        "--message",
        default=DEFAULT_MESSAGE,
        help=f"text to display in the flower center (default: {DEFAULT_MESSAGE!r})",
    )
    args = parser.parse_args(argv)

    animation_file = animation_path(args.message)

    if args.regenerate or not animation_file.exists():
        print(f"Création de l’animation : {animation_file}")
        save_animation(animation_file, args.message)
    else:
        print(f"Lecture de l’animation sauvegardée : {animation_file}")

    play_animation(animation_file)


if __name__ == "__main__":
    main()
