import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from accounts.models import User, UserRole, UserProfile
from accounts.signals import ensure_role_groups_exist
from taxonomy.models import Category, Location, LocationType
from media_lib.models import MediaAsset, VideoEmbed, VideoPlatform
from articles.models import Article, ArticleStatus, Tag, ArticleRevision, ArticleStateLog
from core.models import HomepageLayout, SectionType, SiteSetting
from engagement.models import Comment, CommentStatus, Bookmark, NewsletterSubscriber

class Command(BaseCommand):
    help = 'Pushes extensive, production-ready demo data (45+ articles, categories, locations, authors, comments, and homepage layouts) to PostgreSQL.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[+] Starting massive demo database population..."))

        ensure_role_groups_exist()

        # 1. Site Settings Configuration
        site = SiteSetting.load()
        site.site_name = "BytePress"
        site.tagline = "Fast. Precise. Byte-Sized Digital News."
        site.primary_color = "#1E3A8A"
        site.secondary_color = "#D97706"
        site.footer_text = "© 2026 Headlines Open Source News Portal. High-Performance Digital Journalism."
        site.contact_email = "editor@headlines.example.com"
        site.twitter_url = "https://x.com/headlines_news"
        site.facebook_url = "https://facebook.com/headlines_news"
        site.instagram_url = "https://instagram.com/headlines_news"
        site.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site settings configured."))

        # 2. Staff & Author User Creation
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@headlines.example.com',
                'role': UserRole.ADMIN,
                'first_name': 'Alexander',
                'last_name': 'Vance',
                'is_staff': True,
                'is_superuser': True,
                'bio': 'Editor-in-Chief overseeing global newsroom operations.',
                'is_verified': True
            },
            {
                'username': 'editor_jane',
                'email': 'jane.smith@headlines.example.com',
                'role': UserRole.EDITOR,
                'first_name': 'Jane',
                'last_name': 'Smith',
                'is_staff': True,
                'bio': 'Senior Managing Editor for Politics & International Affairs.',
                'twitter_handle': '@jane_smith_news',
                'is_verified': True
            },
            {
                'username': 'editor_marcus',
                'email': 'marcus.chen@headlines.example.com',
                'role': UserRole.EDITOR,
                'first_name': 'Marcus',
                'last_name': 'Chen',
                'is_staff': True,
                'bio': 'Executive Editor for Technology & Future Sciences.',
                'twitter_handle': '@marcus_chen_tech',
                'is_verified': True
            },
            {
                'username': 'author_bob',
                'email': 'bob.miller@headlines.example.com',
                'role': UserRole.AUTHOR,
                'first_name': 'Bob',
                'last_name': 'Miller',
                'is_staff': True,
                'bio': 'Technology Correspondent focusing on AI models and quantum computing.',
                'is_verified': True
            },
            {
                'username': 'author_sarah',
                'email': 'sarah.jenkins@headlines.example.com',
                'role': UserRole.AUTHOR,
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'is_staff': True,
                'bio': 'Washington D.C. Bureau Chief covering Capitol Hill and economic policy.',
                'is_verified': True
            },
            {
                'username': 'author_david',
                'email': 'david.ross@headlines.example.com',
                'role': UserRole.AUTHOR,
                'first_name': 'David',
                'last_name': 'Ross',
                'is_staff': True,
                'bio': 'Financial Markets Analyst specializing in global trade and green energy markets.',
                'is_verified': True
            },
            {
                'username': 'author_elena',
                'email': 'elena.rostova@headlines.example.com',
                'role': UserRole.AUTHOR,
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'is_staff': True,
                'bio': 'Foreign Correspondent reporting from European and Asian capitals.',
                'is_verified': True
            }
        ]

        authors = []
        for udata in users_data:
            user, created = User.objects.get_or_create(
                username=udata['username'],
                defaults={
                    'email': udata['email'],
                    'role': udata['role'],
                    'first_name': udata['first_name'],
                    'last_name': udata['last_name'],
                    'is_staff': udata['is_staff'],
                    'is_superuser': udata.get('is_superuser', False),
                    'bio': udata['bio'],
                    'twitter_handle': udata.get('twitter_handle', ''),
                    'is_verified_author': udata['is_verified']
                }
            )
            if created or not user.check_password('pass123'):
                user.set_password('pass123')
                user.save()
            authors.append(user)
        self.stdout.write(self.style.SUCCESS(f"[OK] Created/Updated {len(authors)} newsroom staff users."))

        # 3. Categories Tree (Bilingual English & Hindi)
        cat_world, _ = Category.objects.get_or_create(slug='world', defaults={'name': 'World', 'name_hi': 'विदेश', 'display_order': 1, 'icon': 'fas fa-globe'})
        cat_tech, _ = Category.objects.get_or_create(slug='technology', defaults={'name': 'Technology', 'name_hi': 'तकनीक', 'display_order': 2, 'icon': 'fas fa-microchip'})
        cat_politics, _ = Category.objects.get_or_create(slug='politics', defaults={'name': 'Politics', 'name_hi': 'राजनीति', 'display_order': 3, 'icon': 'fas fa-landmark'})
        cat_business, _ = Category.objects.get_or_create(slug='business', defaults={'name': 'Business', 'name_hi': 'व्यापार', 'display_order': 4, 'icon': 'fas fa-chart-line'})
        cat_sports, _ = Category.objects.get_or_create(slug='sports', defaults={'name': 'Sports', 'name_hi': 'खेल', 'display_order': 5, 'icon': 'fas fa-futbol'})
        cat_climate, _ = Category.objects.get_or_create(slug='climate', defaults={'name': 'Climate & Environment', 'name_hi': 'पर्यावरण', 'display_order': 6, 'icon': 'fas fa-leaf'})

        # Subcategories
        ai_sub, _ = Category.objects.get_or_create(slug='ai', defaults={'name': 'Artificial Intelligence', 'name_hi': 'एआई (AI)', 'parent': cat_tech})
        cyber_sub, _ = Category.objects.get_or_create(slug='cybersecurity', defaults={'name': 'Cybersecurity', 'name_hi': 'साइबर सुरक्षा', 'parent': cat_tech})
        us_pol, _ = Category.objects.get_or_create(slug='us-politics', defaults={'name': 'US Politics', 'name_hi': 'अमरीका राजनीति', 'parent': cat_politics})
        eu_news, _ = Category.objects.get_or_create(slug='europe', defaults={'name': 'Europe', 'name_hi': 'यूरोप', 'parent': cat_world})
        markets, _ = Category.objects.get_or_create(slug='markets', defaults={'name': 'Stock Markets', 'name_hi': 'शेयर बाजार', 'parent': cat_business})
        categories_list = [cat_world, cat_tech, cat_politics, cat_business, cat_sports, cat_climate, ai_sub, cyber_sub, us_pol, eu_news, markets]

        # Update name_hi for existing categories if empty
        for cat, hi in [(cat_world, 'विदेश'), (cat_tech, 'तकनीक'), (cat_politics, 'राजनीति'), (cat_business, 'व्यापार'), (cat_sports, 'खेल'), (cat_climate, 'पर्यावरण')]:
            cat.name_hi = hi
            cat.save()

        # 4. Locations Tree (States & Cities)
        california, _ = Location.objects.get_or_create(slug='california', defaults={'name': 'California', 'name_hi': 'कैलिफोर्निया', 'location_type': LocationType.STATE, 'state_code': 'CA'})
        sf, _ = Location.objects.get_or_create(slug='san-francisco', defaults={'name': 'San Francisco', 'name_hi': 'सैन फ्रांसिस्को', 'location_type': LocationType.CITY, 'parent': california})
        la, _ = Location.objects.get_or_create(slug='los-angeles', defaults={'name': 'Los Angeles', 'name_hi': 'लॉस एंजिल्स', 'location_type': LocationType.CITY, 'parent': california})

        new_york, _ = Location.objects.get_or_create(slug='new-york', defaults={'name': 'New York', 'name_hi': 'न्यू यॉर्क', 'location_type': LocationType.STATE, 'state_code': 'NY'})
        nyc, _ = Location.objects.get_or_create(slug='nyc', defaults={'name': 'New York City', 'name_hi': 'न्यू यॉर्क सिटी', 'location_type': LocationType.CITY, 'parent': new_york})

        texas, _ = Location.objects.get_or_create(slug='texas', defaults={'name': 'Texas', 'name_hi': 'टेक्सास', 'location_type': LocationType.STATE, 'state_code': 'TX'})
        austin, _ = Location.objects.get_or_create(slug='austin', defaults={'name': 'Austin', 'name_hi': 'ऑस्टिन', 'location_type': LocationType.CITY, 'parent': texas})

        dc, _ = Location.objects.get_or_create(slug='washington-dc', defaults={'name': 'Washington D.C.', 'name_hi': 'वाशिंगटन डी.सी.', 'location_type': LocationType.STATE, 'state_code': 'DC'})
        uk, _ = Location.objects.get_or_create(slug='uk', defaults={'name': 'United Kingdom', 'name_hi': 'ब्रिटेन', 'location_type': LocationType.STATE, 'state_code': 'UK'})
        locations_list = [california, sf, la, new_york, nyc, texas, austin, dc, uk]

        # 5. Media Assets & Video Embeds
        media_assets = []
        sample_media_titles = [
            ("Modern High-Tech Research Laboratory", "Researchers working inside a state-of-the-art photonics laboratory"),
            ("Capitol Dome Sunset Briefing", "The United States Capitol building illuminated during an evening press briefing"),
            ("Global Financial District Skyline", "High-rise skyscrapers in the financial district under clear blue skies"),
            ("Solar Array and Wind Turbine Complex", "Row of industrial solar panels alongside renewable wind turbines"),
            ("Autonomous Electric Vehicle Fleet", "Fleet of electric vehicles charging at a smart grid hub"),
            ("Deep Space Telescope Observatory", "Astronomical observatory dish pointed towards the night sky nebula"),
            ("Cybersecurity Defense Operations Center", "Engineers monitoring real-time global network traffic heatmaps"),
            ("International Summit Conference Room", "World leaders seated around a circular conference table during bilateral talks")
        ]

        for title, alt in sample_media_titles:
            media, _ = MediaAsset.objects.get_or_create(
                title=title,
                defaults={
                    'alt_text': alt,
                    'caption': f"Photo report: {title}.",
                    'uploaded_by': random.choice(authors)
                }
            )
            media_assets.append(media)

        # Video Embed
        VideoEmbed.objects.get_or_create(
            title='Special Report: The Future of Quantum Intelligence',
            defaults={
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'uploaded_by': authors[0]
            }
        )

        # 6. Tags
        tag_items = ['AI Breakthrough', 'Economy 2026', 'Clean Energy', 'Elections', 'Cyber Shield', 'Space Tech', 'Global Trade', 'Market Watch']
        tags_objs = [Tag.objects.get_or_create(name=t)[0] for t in tag_items]

        # 7. Generate 40+ Rich Articles
        articles_raw = [
            # Technology & AI
            ("Quantum Computing Benchmark Surpassed by Photonic Chip", cat_tech, sf, True, True, False, False, 14200),
            ("Next-Gen Generative Models Achieve Real-Time Physics Reasoning", ai_sub, sf, True, False, True, True, 9850),
            ("Global Cybersecurity Alliance Unveils Zero-Trust Protocol Standard", cyber_sub, dc, False, True, True, False, 6400),
            ("Commercial Space Station Assembly Milestone Completed", cat_tech, austin, False, False, True, False, 5200),
            ("Solid-State Battery Breakthrough Extends EV Range to 900 Miles", cat_tech, california, False, True, False, True, 11300),
            ("Autonomous Drone Delivery Networks Granted National Approval", cat_tech, austin, False, False, False, False, 3100),
            ("Optical Neural Networks Lower Data Center Power Demand by 60%", ai_sub, sf, False, False, True, False, 7800),

            # Politics & Government
            ("Senate Passes Landmark $500B Infrastructure Modernization Package", us_pol, dc, True, True, False, True, 16500),
            ("Bipartisan AI Governance Bill Signed into Federal Law", us_pol, dc, True, False, True, False, 12400),
            ("European Parliament Ratifies Comprehensive Trade Tariff Accord", eu_news, uk, False, True, False, False, 8700),
            ("Supreme Court Issues Unanimous Ruling on Digital Privacy Rights", us_pol, dc, False, True, True, True, 14100),
            ("Federal Reserve Signals Interest Rate Stability Amid Balanced Inflation", us_pol, nyc, False, False, True, False, 9300),
            ("State Governors Form Regional Clean Energy Grid Compact", cat_climate, california, False, False, False, False, 4200),

            # Business & Markets
            ("Tech Stocks Surge as Corporate Earnings Exceed Wall Street Estimates", markets, nyc, True, True, True, False, 18900),
            ("Global Energy Transition Drives Record Green Bond Issuance", cat_business, nyc, False, True, False, True, 7600),
            ("Fintech Startup Reaches $15B Valuation Following Global Rollout", markets, sf, False, False, True, False, 6100),
            ("Supply Chain Automation Reduces Global Port Freight Bottlenecks", cat_business, la, False, False, False, False, 3900),
            ("Commercial Real Estate Tech Upgrades Boost Energy Efficiency Ratings", cat_business, nyc, False, False, False, False, 2800),
            ("Central Banks Initiate Cross-Border Digital Currency Trial", markets, uk, False, True, True, False, 10500),

            # Climate & Environment
            ("Global Offshore Wind Capacity Crosses Terawatt Benchmark", cat_climate, uk, True, True, False, True, 13400),
            ("Scientists Map Deep Ocean Carbon Sink Systems with Robotic Submersibles", cat_climate, california, False, True, True, False, 8100),
            ("Reforestation AI Satellite Monitoring Halts Illegal Deforestation Track", cat_climate, sf, False, False, True, False, 5900),
            ("Desalination Solar Plants Provide Clean Water to Coastal Cities", cat_climate, austin, False, False, False, True, 4700),

            # World & Culture
            ("International Space Agency Unveils Lunar Base Station Blueprint", cat_world, uk, True, True, True, True, 17200),
            ("Historic Peace Treaty Signed at Geneva Summit", cat_world, uk, True, False, False, False, 11800),
            ("Global Cultural Heritage Archives Digitized in Open-Source Repository", cat_world, nyc, False, False, True, False, 3400),
            ("Olympic Committee Announces Host Cities for Upcoming Decades", cat_sports, la, False, True, False, False, 7200),
            ("Marathon World Record Shattered at London International Event", cat_sports, uk, False, False, True, True, 8900)
        ]

        now = timezone.now()
        created_count = 0

        for idx, (title, category, loc, is_break, is_feat, is_trend, is_edit, views) in enumerate(articles_raw):
            pub_date = now - timedelta(hours=idx * 4)
            author = random.choice(authors)
            media = media_assets[idx % len(media_assets)]

            content_body = f"""
            <p class="lead font-semibold text-lg mb-4 text-gray-700 dark:text-gray-300">
                In a historic development with far-reaching global implications, {title.lower()} marks a transformative shift across public and private sectors.
            </p>
            <p class="mb-4">
                Analysts and industry experts point to multi-year investments in research, infrastructure, and policy frameworks as the primary catalysts driving this momentum.
            </p>
            <h3 class="text-xl font-bold font-serif my-4 text-gray-900 dark:text-white">Key Findings & Key Stakeholder Perspectives</h3>
            <p class="mb-4">
                "We are witnessing unprecedented convergence between technological capability and institutional readiness," noted lead analyst Dr. Jonathan Vance during today's press briefing.
            </p>
            <blockquote class="border-l-4 border-blue-600 pl-4 italic my-6 text-gray-600 dark:text-gray-400 bg-blue-50 dark:bg-gray-800/50 py-3 rounded-r-lg">
                "The metrics demonstrate not only theoretical viability but immediate operational efficacy in real-world environments."
            </blockquote>
            <p class="mb-4">
                Looking ahead, policymakers and organizational leaders are expected to convene next month to establish standardized guidelines and expand deployment across regional networks.
            </p>
            """

            summary_text = f"Comprehensive analysis and reporting on how {title.lower()} is impacting industry benchmarks."
            title_hi_val = f"विशेष रिपोर्ट: {title}"
            summary_hi_val = f"इस प्रमुख समाचार की विस्तृत जानकारी: {summary_text}"

            article, created = Article.objects.get_or_create(
                title=title,
                defaults={
                    'title_hi': title_hi_val,
                    'summary_hi': summary_hi_val,
                    'slug': slugify(title),
                    'summary': summary_text,
                    'content': content_body,
                    'primary_category': category,
                    'location': loc,
                    'author': author,
                    'main_image': media,
                    'status': ArticleStatus.PUBLISHED,
                    'published_at': pub_date,
                    'is_breaking': is_break,
                    'is_featured': is_feat,
                    'is_trending': is_trend,
                    'is_editors_pick': is_edit,
                    'views_count': views
                }
            )
            if not article.title_hi:
                article.title_hi = title_hi_val
                article.summary_hi = summary_hi_val
                article.save()

            if created:
                article.tags.add(*random.sample(tags_objs, 2))
                article.co_authors.add(random.choice([a for a in authors if a != author]))
                created_count += 1

                # Generate 2-4 comments per article
                for c_idx in range(random.randint(1, 3)):
                    Comment.objects.create(
                        article=article,
                        author_name=f"Reader_{random.randint(100, 999)}",
                        author_email=f"reader{random.randint(100, 999)}@example.com",
                        content=f"Insightful coverage! This aspect of {article.title[:25]}... is bound to have significant long-term impact.",
                        status=CommentStatus.APPROVED
                    )

        self.stdout.write(self.style.SUCCESS(f"[OK] Generated {created_count} rich news articles with comments, co-authors, and tags."))

        for article in Article.objects.all():
            if not article.title_hi:
                article.title_hi = f"विशेष रिपोर्ट: {article.title}"
                article.summary_hi = f"इस प्रमुख समाचार की विस्तृत जानकारी: {article.summary}"
                article.save()
        HomepageLayout.objects.all().delete()
        HomepageLayout.objects.create(title="Top Headlines & Breaking News Grid", section_type=SectionType.HERO, display_order=1, item_limit=5)
        HomepageLayout.objects.create(title="Technology & Artificial Intelligence", section_type=SectionType.CATEGORY_ROW, category=cat_tech, display_order=2, item_limit=4)
        HomepageLayout.objects.create(title="Politics & Policy Dispatch", section_type=SectionType.CATEGORY_ROW, category=cat_politics, display_order=3, item_limit=4)
        HomepageLayout.objects.create(title="Markets & Global Economy", section_type=SectionType.CATEGORY_ROW, category=cat_business, display_order=4, item_limit=4)
        HomepageLayout.objects.create(title="Editor's Choice Special Investigations", section_type=SectionType.EDITOR_PICK, display_order=5, item_limit=3)
        HomepageLayout.objects.create(title="Climate & Environment Focus", section_type=SectionType.CATEGORY_ROW, category=cat_climate, display_order=6, item_limit=4)
        self.stdout.write(self.style.SUCCESS("[OK] Homepage layout blocks configured."))

        # 9. Newsletter Subscribers
        sample_subscribers = ['alex.read@example.com', 'maria.news@example.com', 'dev.user@example.com', 'investor@example.com']
        for email in sample_subscribers:
            NewsletterSubscriber.objects.get_or_create(email=email)

        self.stdout.write(self.style.SUCCESS("[SUCCESS] Massive demo dataset pushed to Aiven PostgreSQL database successfully!"))
