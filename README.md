# Digital Business Card

Clone:

```
git clone github.com/msimms/DigitalBusinessCard
cd DigitalBusinessCard
```

Create and activate the virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Run:
```
python3 make_card.py --name "John Doe" --phone "555-555-5555" --email "john@doe.com" --org="Acme" --title="CEO" --website="example.com" --logo_path="/Users/Joe/images/logo.png" --social="type=linkedin:https://www.linkedin.com/in/john-doe/" --font_name="Arial"
```
