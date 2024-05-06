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
                            onChange={ () => this.props.appendColor(this.props.id, "no-color") } />
                    <label htmlFor="no-color">No color (dark)</label>
                </div>
                <div>
                    <input type="checkbox" id="rainbow" name="rainbow"
                            onChange={ () => this.props.appendColor(this.props.id, "rainbow") }/>
                    <label htmlFor="rainbow">Rainbow</label>
                </div>
                <div>
                    <input type="checkbox" id="one-color" name="one-color"
                            onChange={ () => {
                                this.props.appendColor(this.props.id, "#000000")
                                this.setState({oneColor: true})
                            }}/>
                    <label htmlFor="one-color">Choose One Color</label>
                </div>
                {
                    (this.state.oneColor)? 
                    <div>
                        <input type="color" onChange={e => this.props.appendColor(this.props.id, e.target.value)} />
                    </div>
                    : ''
                }
            </div>
        )
    }
}