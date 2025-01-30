import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-akretion-storage-deprecated-moved-to-oca",
    description="Meta package for akretion-storage-deprecated-moved-to-oca Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-storage_backend',
        'odoo12-addon-storage_backend_sftp',
        'odoo12-addon-storage_file',
        'odoo12-addon-storage_image',
        'odoo12-addon-storage_image_product',
        'odoo12-addon-storage_thumbnail',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
