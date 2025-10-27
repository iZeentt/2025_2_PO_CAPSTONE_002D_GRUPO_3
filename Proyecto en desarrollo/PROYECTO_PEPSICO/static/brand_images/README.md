Put brand images (logos, banners) in this folder.

Naming suggestions:
- logo.png (primary brand logo, 200x60)
- banner.jpg (hero banner, 1600x400)

These files can be referenced in templates with:

<img src="{{ url_for('static', filename='brand_images/logo.png') }}" alt="Logo">
