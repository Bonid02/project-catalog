from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///inventory.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Items for Appliances Category
category1 = Category(NAME="Appliances", DESCRIPTION="eg. refrigerator, airconditioner, tv..")

session.add(category1)
session.commit()

item1 = Item(NAME="Refrigerator", DESCRIPTION="LG brand 2 door 6 feet",
             QUANTITY=1, CATEGORY_ID=category1.ID, /
             IMAGE_URL='https://image3.mouthshut.com/images/imagesp/925712590s.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Television Small", DESCRIPTION="32 inch, LG Brand",
                     QUANTITY=1, CATEGORY_ID=category1.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Television Big", DESCRIPTION="55 inch, Samsung Brand",
                     QUANTITY=1, CATEGORY_ID=category1.ID, IMAGE_URL='http://takeoffnow.co/wp-content/uploads/2018/01/oled-4k-tv-lg-c7-oled-4k-hdr-smart-tv-55-class-best-oled-4k-tv-deals.jpg')

session.add(item3)
session.commit()

item4 = Item(NAME="Airconditioner", DESCRIPTION="Split type, Mitsubishi Brand",
                     QUANTITY=2, CATEGORY_ID=category1.ID)

session.add(item4)
session.commit()


# Items for Consumables Category
category2 = Category(NAME="Consumables", DESCRIPTION="Drinks and food items")

session.add(category2)
session.commit()

item1 = Item(NAME="Bottled Water", DESCRIPTION="12oz distilled",
                     QUANTITY=36, CATEGORY_ID=category2.ID, IMAGE_URL='http://www.bottledwaterweb.com/upload/members/41_0.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Coca Cola", DESCRIPTION="1.5 Liters",
                     QUANTITY=12, CATEGORY_ID=category2.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="3 in 1 Coffee", DESCRIPTION="Nescafe Brand",
                     QUANTITY=25, CATEGORY_ID=category2.ID, IMAGE_URL='https://www.tazamart.pk/wp-content/uploads/2015/08/Sachets.jpg')

session.add(item3)
session.commit()


# Items for Disposables Category
category3 = Category(NAME="Disposables", DESCRIPTION="Disposable spoons, forks, tissues, cups ..")

session.add(category3)
session.commit()

item1 = Item(NAME="Plastic Cups", DESCRIPTION="3oz size",
                     QUANTITY=200, CATEGORY_ID=category3.ID, IMAGE_URL='https://images-na.ssl-images-amazon.com/images/I/51tWAu4PgUL.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Plastic Spoons", DESCRIPTION="White in color",
                     QUANTITY=300, CATEGORY_ID=category3.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Plastic Forks", DESCRIPTION="White in color",
                     QUANTITY=350, CATEGORY_ID=category3.ID, IMAGE_URL='http://www.castawayfoodpackaging.com.au/wp-content/uploads/2015/10/CA-PCWF_WEB_A.png')

session.add(item3)
session.commit()

item4 = Item(NAME="Bathroom Tissue", DESCRIPTION="Small kept inside storage",
                     QUANTITY=10, CATEGORY_ID=category3.ID)

session.add(item4)
session.commit()

item5 = Item(NAME="Styrophor Cups", DESCRIPTION="For hot beverages",
                     QUANTITY=122, CATEGORY_ID=category3.ID, IMAGE_URL='https://thumbs1.ebaystatic.com/d/l225/m/m8jtKey2bGgWt-dS4C9so5g.jpg')

session.add(item5)
session.commit()


# Items for Electronics Category
category4 = Category(NAME="Electronics", DESCRIPTION="Electric cables, jacks, microphones, extension plugs ..")

session.add(category4)
session.commit()

item1 = Item(NAME="Guitar Cable", DESCRIPTION="8 ft in length, assorted colors",
                     QUANTITY=6, CATEGORY_ID=category4.ID, IMAGE_URL='http://www.musicinstrumentsforeveryone.com/Images/243301/duafire-guitar-cables-professional-noiseless-ultra-flexible-bass-instrument-cables-with-6-35mm-straight-to-straight-plug-for-electric-and-bass-guitar-players-20ft.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Microphone", DESCRIPTION="Shure brand, color black",
                     QUANTITY=3, CATEGORY_ID=category4.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Extension Outlet", DESCRIPTION="6ft in length",
                     QUANTITY=3, CATEGORY_ID=category4.ID, IMAGE_URL='http://cdn2.webninjashops.com/springfieldsas/images/resized/521345880014637398ef637b23e683a52dc9be38.jpg')

session.add(item3)
session.commit()


# Items for Furnitures Category
category5 = Category(NAME="Furnitures", DESCRIPTION="Tables, chairs, cabinets ..")

session.add(category5)
session.commit()

item1 = Item(NAME="Monoblock Chair", DESCRIPTION="White in color",
                     QUANTITY=200, CATEGORY_ID=category5.ID, IMAGE_URL='https://images-na.ssl-images-amazon.com/images/I/51BBkXFC5wL._SY355_.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Long table", DESCRIPTION="6ft folding type",
                     QUANTITY=4, CATEGORY_ID=category5.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Round table", DESCRIPTION="2ft diameter",
                     QUANTITY=1, CATEGORY_ID=category5.ID, IMAGE_URL='http://www.cohoesfarmersmarket.com/thumbnail/a/awesome-48-inch-round-pedestal-table-48-round-pedestal-25.jpeg')

session.add(item3)
session.commit()

item4 = Item(NAME="Office Desk", DESCRIPTION="Wooden brown",
                     QUANTITY=1, CATEGORY_ID=category5.ID)

session.add(item4)
session.commit()


# Items for Lighting Systems Category
category6 = Category(NAME="Lighting Systems", DESCRIPTION="Spot lights, ceiling lights, lamps..")

session.add(category6)
session.commit()

item1 = Item(NAME="Flourescent light", DESCRIPTION="10watts pin type",
                     QUANTITY=35, CATEGORY_ID=category6.ID, IMAGE_URL='https://www.lightonline.com.au/media/catalog/product/cache/1/small_image/400x/602f0fa2c1f0d1ba5e241f914e856ff9/3/2/3276.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Robotic Spot lights", DESCRIPTION="Small black and grey",
                     QUANTITY=4, CATEGORY_ID=category6.ID)


# Items for Musical Instruments Category
category6 = Category(NAME="Musical Instruments", DESCRIPTION="Guitars, drums, piano ..")

session.add(category6)
session.commit()

item1 = Item(NAME="Electric guitar", DESCRIPTION="Fender stratocaster red in color",
                     QUANTITY=1, CATEGORY_ID=category6.ID, IMAGE_URL='https://www.guitarfella.com/wp-content/uploads/2014/07/Squier-by-Fender-Classic-Vibe-50%E2%80%99s-Telecaster-300-e1425940032334.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Snare Drum", DESCRIPTION="Tama brand",
                     QUANTITY=1, CATEGORY_ID=category6.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Synthesizer", DESCRIPTION="48 keys Roland",
                     QUANTITY=1, CATEGORY_ID=category6.ID, IMAGE_URL='https://images-na.ssl-images-amazon.com/images/I/512tfuDFOqL._SX425_.jpg')

session.add(item3)
session.commit()

item4 = Item(NAME="Keyboard Piano", DESCRIPTION="64 keys Kurzwell",
                     QUANTITY=1, CATEGORY_ID=category6.ID)

session.add(item4)
session.commit()


# Items for Ornaments Category
category7 = Category(NAME="Ornaments", DESCRIPTION="Curtains, decors, banners ..")

session.add(category7)
session.commit()

item1 = Item(NAME="Banner", DESCRIPTION="8ft assemble type",
                     QUANTITY=2, CATEGORY_ID=category7.ID, IMAGE_URL='https://sc02.alicdn.com/kf/HTB1qEzPbi0TMKJjSZFNq6y_1FXaw/Popular-Horizontal-Banner-Foldable-Roll-Up-Banner.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Curtain", DESCRIPTION="Black 12ft",
                     QUANTITY=8, CATEGORY_ID=category7.ID)

session.add(item2)
session.commit()


# Items for Office Supplies Category
category8 = Category(NAME="Office Supplies", DESCRIPTION="Paper, envelopes, pens ..")

session.add(category8)
session.commit()

item1 = Item(NAME="Ballpen", DESCRIPTION="Assorted color and brand",
                     QUANTITY=50, CATEGORY_ID=category8.ID, IMAGE_URL='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/4_Bic_Cristal_pens_and_caps.jpg/220px-4_Bic_Cristal_pens_and_caps.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Bond Paper", DESCRIPTION="A4 size",
                     QUANTITY=300, CATEGORY_ID=category8.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Scotch tape", DESCRIPTION="2in thick",
                     QUANTITY=5, CATEGORY_ID=category8.ID, IMAGE_URL='https://cdnimg.webstaurantstore.com/images/products/large/46404/411409.jpg')

session.add(item3)
session.commit()


# Items for Sound Systems Category
category9 = Category(NAME="Sound Systems", DESCRIPTION="Speakers, amplifiers, monitors ..")

session.add(category9)
session.commit()

item1 = Item(NAME="House Speaker", DESCRIPTION="300 Watts Yamaha",
                     QUANTITY=4, CATEGORY_ID=category9.ID, IMAGE_URL='http://vbizz.com/images/products/6516/thumb/783460994.g_0-w_g_s500.jpg')

session.add(item1)
session.commit()

item2 = Item(NAME="Guitar Amplifier", DESCRIPTION="200watts Marshall",
                     QUANTITY=1, CATEGORY_ID=category9.ID)

session.add(item2)
session.commit()

item3 = Item(NAME="Bass Amplifier", DESCRIPTION="250watts Hartke",
                     QUANTITY=1, CATEGORY_ID=category9.ID, IMAGE_URL='https://images-na.ssl-images-amazon.com/images/I/81aSejxDcBL._SX355_.jpg')

session.add(item3)
session.commit()



print "Sample Item Data Added"
