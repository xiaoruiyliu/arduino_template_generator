import numpy as np
class Template():
    def __init__(self, hardware, num_leds, colors, num_buttons = None, sensor_boundary = None):
        self.hardware = hardware
        self.num_leds = num_leds
        # colors should be a list of user input (for example a sensor will have a list of two elements [(333,333,333), "rainbow"]
        # this represents the user wants an rgb specification for the < boundary and rainbow for > boundary
        # for default, should just be a list with one entry, ex: [(222, 222, 222)], off maps to "clear", and rainbow maps to "rainbow"
        # for buttons, it should be a list of values [clear, rainbow]
        self.colors = colors
        if hardware == "button":
            self.num_buttons = num_buttons
        if hardware == "sensor":
            self.sensor_boundary = sensor_boundary

    def synthesize_program(self):
        return self.get_prelude() + self.get_setup() + self.get_loop() + self.get_additional_functions()

    def get_prelude(self):
        define_leds = "\n#define NUM_OF_LED " + str(self.num_leds)
        prelude = "#include <Adafruit_NeoPixel.h>" + define_leds + "\n#define PIXEL_PIN    6\n//global\nAdafruit_NeoPixel strip(NUM_OF_LED, PIXEL_PIN, NEO_GRB + NEO_KHZ800);\nHARDWARE_PRELUDE"
        if self.hardware == "button":
            dependent = self.get_prelude_buttons()
            return prelude + dependent
        elif self.hardware == "sensor":
            dependent = self.get_prelude_sensor()
            return prelude + dependent
        elif self.hardware == "default":
            return prelude

    def get_prelude_buttons(self):
        compiled = ""
        for i in range(1, self.num_buttons + 1):
            compiled += f"\ndefine BUTTON_PIN_{i} //pin for the button no. {i}\nint button_val_{i} = 0;\nint prev_button_val_{i} = 0;"
        return compiled

    def get_prelude_sensor(self):
        compiled = "\n#define ULTRASONIC_TRIG_PIN 9\n#define ULTRASONIC_ECHO_PIN 10\nfloat duration, distance;"
        compiled += f"\n int boundary = {self.sensor_boundary};"
        return compiled

    def get_setup(self):
        setup = "\nvoid setup() {HARDWARE_DEPENDENCY\n\tstrip.begin();\n\tstrip.show();\n}"
        if self.hardware == "button":
            dependent = self.get_setup_buttons()
        elif self.hardware == "sensor":
            dependent = self.get_setup_sensor()
        elif self.hardware == "default":
            dependent = ""
        return setup.replace("HARDWARE_DEPENDENCY", dependent)

    def get_setup_buttons(self):
        compiled = ""
        for i in range(1, self.num_buttons + 1):
            compiled += f"\n\tpinMode(BUTTON_PIN_{i}, OUTPUT);"
        return compiled

    def get_setup_sensor(self):
        return "\n\tpinMode(ULTRASONIC_TRIG_PIN, OUTPUT);\n\tpinMode(ULTRASONIC_ECHO_PIN, INPUT);\n\tSerial.begin(9600);"

    def get_loop(self):
        # complete the loop (not sure how completed loop would look like)
        # TODO
        return ""

    def get_color_logic(self):
        compiled = ""
        if self.hardware == "button":
            for i in range(1, self.num_buttons + 1):
                snippet = f"\n\tif (!prev_button_val_{i} && button_val_{i})"
                snippet += " {"
                snippet += self.get_specific_color_logic(self.colors[i - 1])
                snippet += "\n\t}"
                compiled += snippet
        elif self.hardware == "sensor":
            snippet = ("\n\tdigitalWrite(ULTRASONIC_TRIG_PIN, LOW);\n\tdelayMicroseconds(2);\n\tdigitalWrite("
                       "ULTRASONIC_TRIG_PIN, HIGH);\n\tdelayMicroseconds(10);\n\tdigitalWrite(ULTRASONIC_TRIG_PIN, "
                       "LOW);\n\tduration = pulseIn(ULTRASONIC_ECHO_PIN, HIGH);\n\tdistance = duration * 0.034 / 2; "
                       "//distance in cm\n\tSerial.print(\"Distance: \");\n\tSerial.println(distance);")
            snippet += "\n\tif (distance < boundary) {"
            snippet += self.get_specific_color_logic(self.colors[0])
            snippet += "\n\t}"
            snippet += "\n\telse {"
            snippet += self.get_specific_color_logic(self.colors[1])
            snippet += "\n\t}"
            compiled += snippet
        elif self.hardware == "default":
            compiled += self.get_specific_color_logic(self.colors[0])
        return compiled

    def get_specific_color_logic(self, desired_output):
        if desired_output is tuple:
            r, g, b = desired_output[0], desired_output[1], desired_output[2]
            return f"\n\t\tcolorWipe(strip.Color(  {r}, {g}, {b}), 50); //the number 50 determines how fast the color changes"
        if desired_output == "rainbow":
            return "\n\t\ttheaterChaseRainbow(50);"
        if desired_output == "clear":
            return "\n\t\tstrip.clear();\n\t\tstrip.show();"

    def get_additional_functions(self):
        compiled = ""
        if "rainbow" in np.array(self.colors).flatten():
            compiled += ("\nvoid theaterChaseRainbow(int wait) {\n\tint firstPixelHue = 0;\n\tfor(int a=0; a<30; a++) {  // "
                    "Repeat 30 times...\n\t\tfor(int b=0; b<3; b++) {\n\t\t\tstrip.clear();\n\t\t\tfor(int c=b; "
                    "c<strip.numPixels(); c += 3) {\n\t\t\t\tint hue = firstPixelHue + c * 65536L / strip.numPixels("
                    ");\n\t\t\t\tuint32_t color = strip.gamma32(strip.ColorHSV(hue));\n\t\t\t\tstrip.setPixelColor(c, "
                    "color);\n\t\t\t}\n\t\t\tstrip.show();\n\t\t\tdelay(wait);\n\t\t\tfirstPixelHue += 65536 / "
                    "90;\n\t\t}\n\t}\n}")
        if tuple in np.array(self.colors).flatten():
            compiled += ("\nvoid colorWipe(uint32_t color, int wait) {\n\tfor(int i=0; i<strip.numPixels(); i++) { // "
                         "For each pixel in strip...\n\t\tstrip.setPixelColor(i, color);         //  Set pixel's "
                         "color (in RAM)\n\t\tstrip.show();                          //  Update strip to "
                         "match\n\t\tdelay(wait);                           //  Pause for a moment\n\t}\n}")
        return compiled
