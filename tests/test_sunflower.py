import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops

import Sunflower2


class SunflowerTests(unittest.TestCase):
    def test_image_point_converts_centered_coordinates(self):
        self.assertEqual(Sunflower2.image_point((0, 0)), (450, 450))
        self.assertEqual(Sunflower2.image_point((10, 20)), (460, 430))

    def test_leaf_points_form_a_closed_polygon(self):
        points = Sunflower2.leaf_points((0, 0), 45)

        self.assertEqual(len(points), 42)
        self.assertEqual(points[0], points[-1])

    def test_animation_has_consistent_frames_and_durations(self):
        frames, durations = Sunflower2.draw_animation()

        self.assertEqual(len(frames), 90)
        self.assertEqual(len(frames), len(durations))
        self.assertTrue(all(frame.size == (900, 900) for frame in frames))

    def test_custom_message_changes_final_frame(self):
        default_frames, _ = Sunflower2.draw_animation()
        custom_frames, _ = Sunflower2.draw_animation("Welcome to the project")

        difference = ImageChops.difference(
            default_frames[-1].convert("RGB"),
            custom_frames[-1].convert("RGB"),
        )
        self.assertIsNotNone(difference.getbbox())

    def test_animation_path_is_stable_and_separate_per_message(self):
        self.assertEqual(
            Sunflower2.animation_path(Sunflower2.DEFAULT_MESSAGE),
            Sunflower2.ANIMATION_FILE,
        )
        first_path = Sunflower2.animation_path("Hello, Alex")
        self.assertEqual(first_path, Sunflower2.animation_path("Hello, Alex"))
        self.assertNotEqual(first_path, Sunflower2.animation_path("Hello, Sam"))
        self.assertNotEqual(first_path, Sunflower2.ANIMATION_FILE)

    def test_save_animation_writes_a_complete_gif(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "animation.gif"

            Sunflower2.save_animation(path)

            with Image.open(path) as animation:
                self.assertEqual(animation.format, "GIF")
                self.assertEqual(animation.size, (900, 900))
                self.assertEqual(animation.n_frames, 90)
            self.assertFalse(path.with_name("animation.tmp.gif").exists())

    def test_main_reuses_existing_animation(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "animation.gif"
            path.touch()

            with (
                patch.object(Sunflower2, "ANIMATION_FILE", path),
                patch.object(Sunflower2, "save_animation") as save_animation,
                patch.object(Sunflower2, "play_animation") as play_animation,
            ):
                Sunflower2.main([])

            save_animation.assert_not_called()
            play_animation.assert_called_once_with(path)

    def test_custom_message_uses_its_own_saved_animation(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "animation.gif"
            message_hash = hashlib.sha256(b"Hello, Alex").hexdigest()[:12]
            custom_path = path.with_name(
                f"{path.stem}-{message_hash}{path.suffix}"
            )
            custom_path.touch()

            with (
                patch.object(Sunflower2, "ANIMATION_FILE", path),
                patch.object(Sunflower2, "play_animation") as play_animation,
                patch.object(Sunflower2, "save_animation") as save_animation,
            ):
                Sunflower2.main(["--message", "Hello, Alex"])

            save_animation.assert_not_called()
            play_animation.assert_called_once_with(custom_path)

    def test_regenerate_option_replaces_existing_animation(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "animation.gif"

            with (
                patch.object(Sunflower2, "ANIMATION_FILE", path),
                patch.object(Sunflower2, "save_animation") as save_animation,
                patch.object(Sunflower2, "play_animation"),
            ):
                Sunflower2.main(["--regenerate"])

            save_animation.assert_called_once_with(path, "Hello world")


if __name__ == "__main__":
    unittest.main()
