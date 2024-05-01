import React from "react";
import ColorPicker from "./ColorPicker";

const Questions = {
    "N": {
        q: "Number of LEDs",
        type: "number",
        options: "",
        id: "n_of_led",
        next: "Hardware"
    },
    "Hardware": {
        q: "Connected hardware (choose one)",
        type: "checkbox",
        options: ["No other hardware", "Buttons", "Ultrasonic Sensor"],
        id: "hardware",
        next: "hardware options"
    },
    "Buttons": {
        q: "How many buttons do you have? (1-5)",
        type: "number",
        options: [],
        id: "n_of_buttons",
        next: "Buttons-Color"
    },
    "Buttons-Color": {
        q: "What color does each button correspond to?",
        type: "color",
        options: [],
        id: "color_of_buttons",
        next: "end"
    },
    "Ultrasonic Sensor": {
        q: "What is the max distance to trigger the change of color? (in centimeters)",
        type: "number",
        options: "",
        id: "ultrasonic_boundary",
        next: "Ultrasonic-Color1"
    },
    "Ultrasonic-Color1": {
        q: "What is the color for the shorter distance?",
        type: "color",
        options: "",
        id: "ultrasonic_color1",
        next: "Ultrasonic-Color2"
    },
    "Ultrasonic-Color2": {
        q: "What is the color for the longer distance?",
        type: "color",
        options: "",
        id: "ultrasonic_color2",
        next: "end"
    },
    "No other hardware": {
        q: "What is the color of the LED strip?",
        type: "color",
        options: "",
        id: "no_hardware_color",
        next: "end"
    }
}

export default class Main extends React.Component {
    constructor(props){
        super(props)
        this.state = {
                        n_of_led: 0,
                        hardware: "",
                        n_of_buttons: 0,
                        color_of_buttons: [],
                        ultrasonic_boundary: 0,
                        ultrasonic_color1: "",
                        ultrasonic_color2: "",
                        no_hardware_color: "",
                        current_q: "N",
                    }
    }
    getAnswer(e, id) {
        this.setState({ [id] :e.target.value})   
    }
    getOption(id, name){
        this.setState({ [id]: name})
    }
    nextQuestion(next) {
        console.log(next)
        if (next === "hardware options") {
            console.log("here")
            var hardware = this.state.hardware
            console.log(hardware)
            this.setState({current_q: hardware})
        }
        else this.setState({current_q: next})
    }
    render () {
        console.log(this.state)
        if (this.state.current_q === "end") {
            return (
                <div>
                    DONE!
                </div>
            )
        }
        var question = Questions[this.state.current_q]
        var answer_options = ""
        if (question.type === "number"){
            answer_options = <input type="number" onChange={ e => this.getAnswer(e, question.id)} />
        }
        else if (question.type === "checkbox") {
            var option = question.options
            answer_options = <div>
                                <div>
                                    <input type="checkbox" id={option[0]} name={option[0]}
                                            onChange={ () => this.getOption(question.id , option[0]) } />
                                    <label htmlFor={option[0]}>{option[0]}</label>
                                </div>
                                <div>
                                    <input type="checkbox" id={option[1]} name={option[1]}
                                             onChange={ () => this.getOption(question.id, option[1]) }/>
                                    <label htmlFor={option[1]}>{option[1]}</label>
                                </div>
                                <div>
                                    <input type="checkbox" id={option[2]} name={option[2]}
                                            onChange={ () => this.getOption(question.id, option[2]) }/>
                                    <label htmlFor={option[2]}>{option[2]}</label>
                                </div>
                            </div>
        }
        else if (this.state.current_q === "Buttons-Color") {
            var multiple_colors = []
            for(var i=0; i<this.state.n_of_buttons; i++) {
                multiple_colors.push(
                    <div>
                        <h3>What is the color of button {i+1}?</h3>
                        <ColorPicker/>
                    </div>
                    
                )
            } 
            answer_options = <div>{multiple_colors}</div>

        }
        else if (question.type === "color") {
            answer_options = <ColorPicker />
        }
        return (
            <div>
                <h1>{question.q}</h1>
                {answer_options}
                <button onClick={() => this.nextQuestion(question.next)}>
                    ok
                </button>
            </div>
        )
    }
}
