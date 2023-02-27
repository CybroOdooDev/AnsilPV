{
    'name': 'Theme Mars',
    'description': 'Theme Mars is an attractive and modern Website theme',
    'summary': 'Theme Mars is a new kind of Theme. '
               'The theme is a very user-friendly and is suitable for your website.',
    'category': 'Theme',
    'version': '16.0.1.0.0',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'website'],
    'data': [
        'views/theme_snippet.xml',
        'views/theme_template_header.xml',
        'views/theme_template_footer.xml',
        'views/layouts.xml',
        'views/theme_template_about.xml',
        'views/theme_template_userlogin.xml',
        'views/theme_shop_cart.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            "theme_mars/static/src/css/style.css",
            "/theme_mars/static/src/js/owl.carousel.js",
            "/theme_mars/static/src/js/jquery.appear.min.js",
            "/theme_mars/static/src/js/jquery.easypiechart.min.js",
            # "/theme_mars/static/src/js/bootstrap.min.js",
            # "/theme_mars/static/src/js/jquery-2.2.4.min.js",
            "/theme_mars/static/src/js/custom.js",
            # "/theme_mars/static/src/js/options.js",
            "theme_mars/static/src/js/owl.carousel.min.js",
            # "theme_mars/static/src/js/action_manager.js",
            # "theme_mars/static/src/Images/partners/p (1).png",
        ],
        'website.assets_wysiwyg': [
            "/theme_mars/static/src/js/snippets/options.js",
        ]
    },
    # 'images': [
    #     'static/src/Images/partners/p (1).png',
    #     'static/src/Images/team/team (3).jpg',
    #     # 'static/description/theme_screenshot.png',
    # ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
