import numpy as np

class Template():
    def __init__(self, hardware, num_leds,
        button_colors, num_buttons,
        sensor_color1, sensor_color2, sensor_boundary,
        no_hardware_color):
        
        '''
        n_of_led: 0,
        hardware: "",
        n_of_buttons: 0,
        color_of_buttons: [],
        ultrasonic_boundary: 0,
        ultrasonic_color1: "",
        ultrasonic_color2: "",
        no_hardware_color: "",
        '''
        self.BUTTONS = "Buttons"
        self.SENSOR = "Ultrasonic Sensor"
        self.DEFAULT = "No other hardware"
        
        self.hardware = hardware
        self.num_leds = int(num_leds)
        # colors should be a list of user input (for example a sensor will have a list of two elements [(333,333,333), "rainbow"]
        # this represents the user wants an rgb specification for the < boundary and rainbow for > boundary
        # for default, should just be a list with one entry, ex: [(222, 222, 222)], off maps to "clear", and rainbow maps to "rainbow"
        # for buttons, it should be a list of values [clear, rainbow]
        if button_colors != '':
            self.colors = button_colors
        elif sensor_color1 != '':
            self.colors = sensor_color1 + ',' + sensor_color2
        else:
            self.colors = no_hardware_color

        self.colors = self.colors.split(',')

        print(self.colors)

        def hex_to_rgb(hex):
            return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

        for i in range(len(self.colors)):
            color = self.colors[i]
            if color != "rainbow" and color != "no-color":
                self.colors[i] = hex_to_rgb(color[1:])



        print(self.colors)

        if hardware == self.BUTTONS:
            self.num_buttons = int(num_buttons)
        if hardware == self.SENSOR:
            self.sensor_boundary = int(sensor_boundary)

    def synthesize_program(self):
        print("get_prelude")
        print(self.get_prelude())
        print("get_setup")
        print(self.get_setup())
        print("get_loop")
        print(self.get_loop())
        print("get_additional_functions")
        print(self.get_additional_functions())
        ret = self.get_prelude() + "\n" + self.get_setup() + "\n" + self.get_loop() + "\n" + self.get_additional_functions()
        print(ret)
        return ret

    def get_prelude(self):
        define_leds = "\n#define NUM_OF_LED " + str(self.num_leds)
        prelude = "#include <Adafruit_NeoPixel.h>" + define_leds + "\n#define PIXEL_PIN 6\n\n\n//global\nAdafruit_NeoPixel strip(NUM_OF_LED, PIXEL_PIN, NEO_GRB + NEO_KHZ800);\nHARDWARE_PRELUDE"
        if self.hardware == self.BUTTONS:
            dependent = self.get_prelude_buttons()
            return prelude.replace("HARDWARE_PRELUDE", dependent)
        elif self.hardware ==self.SENSOR:
            dependent = self.get_prelude_sensor()
            return prelude.replace("HARDWARE_PRELUDE", dependent)
        elif self.hardware == self.DEFAULT:
            return prelude.replace("HARDWARE_PRELUDE", '')

    def get_prelude_buttons(self):
        compiled = ""
        for i in range(1, self.num_buttons + 1):
            compiled += f"\n#define BUTTON_PIN_{i} {i+6} //pin for the button no. {i}\nint button_val_{i} = 0;\nint prev_button_val_{i} = 0;\n"
        return compiled

    def get_prelude_sensor(self):
        compiled = "\n#define ULTRASONIC_TRIG_PIN 9\n#define ULTRASONIC_ECHO_PIN 10\nfloat duration, distance;"
        compiled += f"\n int boundary = {self.sensor_boundary};"
        return compiled

    def get_setup(self):
        setup = "\nvoid setup() {\nHARDWARE_DEPENDENCY\n\tstrip.begin();\n\tstrip.show();\n\n\t}"
        if self.hardware == self.BUTTONS:
            dependent = self.get_setup_buttons()
        elif self.hardware == self.SENSOR:
            dependent = self.get_setup_sensor()
        elif self.hardware == self.DEFAULT:
            dependent = ""
        return setup.replace("HARDWARE_DEPENDENCY", dependent)

    def get_setup_buttons(self):
        compiled = ""
        for i in range(1, self.num_buttons + 1):
            compiled += f"\n\tpinMode(BUTTON_PIN_{i}, OUTPUT);\n"
        return compiled

    def get_setup_sensor(self):
        return "\n\tpinMode(ULTRASONIC_TRIG_PIN, OUTPUT);\n\tpinMode(ULTRASONIC_ECHO_PIN, INPUT);\n\tSerial.begin(9600);"

    def get_loop(self):
        loop = "\nvoid loop() {\nLOOP_DEPENDENCY\n}"
        dependent = self.get_color_logic()
        return loop.replace("LOOP_DEPENDENCY", dependent)

    def get_color_logic(self):
        compiled = ""
        if self.hardware == self.BUTTONS:
            for i in range(1, self.num_buttons + 1):
                snippet = f"\n\tif (!prev_button_val_{i} && button_val_{i})"
                snippet += " {"
                snippet += "\n\t" + self.get_specific_color_logic(self.colors[i - 1])
                snippet += "\n\t}\n"
                snippet += f"\n\tprev_button_val_{i} = button_val_{i};\n\tbutton_val_{i} = digitalRead(BUTTON_PIN_{i});\n"
                compiled += snippet
        elif self.hardware == self.SENSOR:
            snippet = ("\n\tdigitalWrite(ULTRASONIC_TRIG_PIN, LOW);\n\tdelayMicroseconds(2);\n\tdigitalWrite("
                       "ULTRASONIC_TRIG_PIN, HIGH);\n\tdelayMicroseconds(10);\n\tdigitalWrite(ULTRASONIC_TRIG_PIN, "
                       "LOW);\n\tduration = pulseIn(ULTRASONIC_ECHO_PIN, HIGH);\n\tdistance = duration * 0.034 / 2; "
                       "//distance in cm\n\tSerial.print(\"Distance: \");\n\tSerial.println(distance);")
            snippet += "\n\tif (distance < boundary) {"
            snippet += "\n\t\t" + self.get_specific_color_logic(self.colors[0])
            snippet += "\n\t}"
            snippet += "\n\telse {"
            snippet += "\n\t\t" + self.get_specific_color_logic(self.colors[1])
            snippet += "\n\t}"
            compiled += snippet
        elif self.hardware == self.DEFAULT:
            compiled += "\n" + self.get_specific_color_logic(self.colors[0])
        return compiled

    def get_specific_color_logic(self, desired_output):
        if type(desired_output) is tuple:
            r, g, b = desired_output[0], desired_output[1], desired_output[2]
            return f"\tcolorWipe(strip.Color({r}, {g}, {b}), 50); //the number 50 determines how fast the color changes"
        if desired_output == "rainbow":
            return "\ttheaterChaseRainbow(50);"
        if desired_output == "no-color":
            return "\tstrip.clear();\n\t\tstrip.show();"

    def get_additional_functions(self):
        compiled = ""
        if "rainbow" in self.colors:
            compiled += ("\nvoid theaterChaseRainbow(int wait) {\n\tint firstPixelHue = 0;\n\tfor(int a=0; a<30; a++) {  // "
                    "Repeat 30 times...\n\t\tfor(int b=0; b<3; b++) {\n\t\t\tstrip.clear();\n\t\t\tfor(int c=b; "
                    "c<strip.numPixels(); c += 3) {\n\t\t\t\tint hue = firstPixelHue + c * 65536L / strip.numPixels("
                    ");\n\t\t\t\tuint32_t color = strip.gamma32(strip.ColorHSV(hue));\n\t\t\t\tstrip.setPixelColor(c, "
                    "color);\n\t\t\t}\n\t\t\tstrip.show();\n\t\t\tdelay(wait);\n\t\t\tfirstPixelHue += 65536 / "
                    "90;\n\t\t}\n\t}\n}")
        if tuple in self.colors:
            compiled += ("\nvoid colorWipe(uint32_t color, int wait) {\n\tfor(int i=0; i<strip.numPixels(); i++) { // "
                         "For each pixel in strip...\n\t\tstrip.setPixelColor(i, color);         //  Set pixel's "
                         "color (in RAM)\n\t\tstrip.show();                          //  Update strip to "
                         "match\n\t\tdelay(wait);                           //  Pause for a moment\n\t}\n}")
        compiled += ("\nvoid colorWipe(uint32_t color, int wait) {\n\tfor(int i=0; i<strip.numPixels(); i++) {//" 
                    "For each pixel in strip...\n\t\tstrip.setPixelColor(i, color);         //  Set pixel's color"
                    "\n\t\tstrip.show();                          //  Update strip to match"
                    "\n\t\tdelay(wait);                           //  Pause for a moment\n\t}\n}\n")
        return compiled
