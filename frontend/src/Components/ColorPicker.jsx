import React from "react";

export default class ColorPicker extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            color: "",
            oneColor: false
        }
    }
    render(){
        console.log(this.state)
        return (
            <div>
                <div>
                    <input type="checkbox" id="no-color" name="no-color"
                            onChange={ () => this.setState({color: "no-color"}) } />
                    <label htmlFor="no-color">No color (dark)</label>
                </div>
                <div>
                    <input type="checkbox" id="rainbow" name="rainbow"
                            onChange={ () => this.setState({color: "rainbow"}) }/>
                    <label htmlFor="rainbow">Rainbow</label>
                </div>
                <div>
                    <input type="checkbox" id="one-color" name="one-color"
                            onChange={ () => this.setState({oneColor: true}) }/>
                    <label htmlFor="one-color">Choose One Color</label>
                </div>
                {
                    (this.state.oneColor)? 
                    <div>
                        <input type="color" onChange={e => this.setState({color: e.target.value})} />
                    </div>
                    : ''
                }
            </div>
        )
    }
}