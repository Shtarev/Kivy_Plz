import kivy
import requests
import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

url = ''
capitals = {
    'Andorra': 'AD',
    'Argentina': 'AR',
    'American Samoa': 'AS',
    'Austria': 'AT',
    'Australia': 'AU',
    'Bangladesh': 'BD',
    'Belgium': 'BE',
    'Bulgaria': 'BG',
    'Brazil': 'BR',
    'Canada': 'CA',
    'Switzerland': 'CH',
    'Czech Republic': 'CZ',
    'Germany': 'DE',
    'Denmark': 'DK',
    'Dominican Republic': 'DO',
    'Spain': 'ES',
    'Finland': 'FI',
    'Faroe Islands': 'FO',
    'France': 'FR',
    'Great Britain': 'GB',
    'French Guyana': 'GF',
    'Guernsey': 'GG',
    'Greenland': 'GL',
    'Guadeloupe': 'GP',
    'Guatemala': 'GT',
    'Guam': 'GU',
    'Guyana': 'GY',
    'Croatia': 'HR',
    'Hungary': 'HU',
    'Isle of Man': 'M',
    'India': 'IN',
    'Iceland': 'IS',
    'Italy': 'IT',
    'Jersey': 'JE',
    'Japan': 'JP',
    'Liechtenstein': 'LI',
    'Sri Lanka': 'LK',
    'Lithuania': 'LT',
    'Luxembourg': 'LU',
    'Monaco': 'MC',
    'Moldavia': 'MD',
    'Marshall Islands': 'MH',
    'Macedonia': 'MK',
    'Northern Mariana Islands': 'MP',
    'Martinique': 'MQ',
    'Mexico': 'MX',
    'Malaysia': 'MY',
    'Holland': 'NL',
    'Norway': 'NO',
    'New Zealand': 'NZ',
    'Phillippines': 'PH',
    'Pakistan': 'PK',
    'Poland': 'PL',
    'Saint Pierre and Miquelon': 'PM',
    'Puerto Rico': 'PR',
    'Portugal': 'PT',
    'French Reunion': 'RE',
    'Russia': 'RU',
    'Sweden': 'SE',
    'Slovenia': 'SI',
    'Svalbard & Jan Mayen Islands': 'SJ',
    'Slovak Republic': 'SK',
    'San Marino': 'SM',
    'Thailand': 'TH',
    'Turkey': 'TR',
    'United States': 'US',
    'Vatican': 'VA',
    'Virgin Islands': 'VI',
    'Mayotte': 'YT',
    'South Africa': 'ZA'
}

class Plz_Widget(Widget):

    def __init__(self, **kwargs):
        super(Plz_Widget, self).__init__(**kwargs)
        
        layout = RelativeLayout(size = (Window.width, Window.height))
        self.add_widget(layout)
        
        dropdown = DropDown(max_height = 300)
        for key in capitals:
            btnLand = Button(text = key,
                             size_hint_y = None,
                             height = 50)
            
            btnLand.bind(on_release = lambda btnLand: dropdown.select(btnLand.text))
            dropdown.add_widget(btnLand)

        self.selectCountry = Button(text ='Select a country',
                            size_hint =(.3, .1),
                            pos_hint = {'center_x':.5, 'center_y':.65})
        self.selectCountry.bind(on_release = dropdown.open)
        dropdown.bind(on_select = lambda instance, x: setattr(self.selectCountry, 'text', x))
        layout.add_widget(self.selectCountry)
        
        self.labelPlz = Label(text ="Enter a postal code",
                    font_size = 25,
                    pos_hint = {'center_x':.5, 'center_y':.9})
        layout.add_widget(self.labelPlz)

        self.inptPlz = TextInput(text ="",
                    font_size = 35,
                    size_hint =(.3, .1),
                    height = 100,
                    multiline = False,
                    pos_hint = {'center_x':.5, 'center_y':.8})
        layout.add_widget(self.inptPlz)

        btn = Button(text='Go!',
                     size_hint =(.3, .1),
                     pos_hint = {'center_x':.5, 'center_y':.5},
                     background_color = '#0066FF')
        btn.bind(on_press=self.handlerApi)
        layout.add_widget(btn)
        
        self.anzeige = Label(text='Result:',
                             size = (Window.width, 100),
                             text_size = (Window.width, None),
                             pos_hint = {'x':.05, 'center_y':.1},
                             color = '#FFFFFF'
                             )
        layout.add_widget(self.anzeige)

    def handlerApi(self, instance):
        if self.selectCountry.text == 'Select a country':
            self.anzeige.color = '#FF6600'
            self.anzeige.text = 'Warning:\nSelect a country'
        elif self.inptPlz.text == '':
            self.anzeige.color = '#FF6600'
            self.anzeige.text = 'Warning:\nEnter a postal code'
        else:
            self.anzeige.color = '#FFFFFF'
            url = 'https://api.zippopotam.us/%s/%s' % (capitals[self.selectCountry.text], self.inptPlz.text)
            res = requests.get(url)
            if res.status_code != 200:
                self.anzeige.text = 'Result:\nRequest error. Code: ' + str(res.status_code)
            else:
                data_json = json.loads(res._content)
                self.anzeige.text =  'Result:\nCountry: ' + data_json['country'] + '\nState: ' + data_json['places'][0]['state'] + '\nCity: ' + data_json['places'][0]['place name']

class ApiApp(App):
    def build(self):
        return Plz_Widget()

if __name__ == "__main__":
    ApiApp().run()
