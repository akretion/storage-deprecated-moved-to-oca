import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-akretion-storage-deprecated-moved-to-oca",
    description="Meta package for akretion-storage-deprecated-moved-to-oca Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-storage_backend',
        'odoo8-addon-storage_file',
        'odoo8-addon-storage_image',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
