from main import serve_file


@serve_file.route("/profile_images/<string:filename>", strict_slashes=False, methods=["GET"])
def get_profile_images(filename: str):
    """Return profile image"""
    return serve_file.send_static_file(f"profile_images/{filename}")