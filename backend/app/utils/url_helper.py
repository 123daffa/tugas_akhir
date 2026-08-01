def ensure_url(url: str) -> str:
    """Pastikan URL selalu punya prefix https://, dipakai bersama oleh
    run_text_pipeline, image_pipeline, dan video_pipeline supaya konsisten
    -- daripada didefinisikan ulang atau di-import silang antar pipeline."""
    if not url:
        return '#'
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url