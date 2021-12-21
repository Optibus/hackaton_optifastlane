
import './App.css';
import { TimePicker } from 'antd';
import moment from 'moment';
import "antd/dist/antd.css";
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Button, Form } from 'react-bootstrap';
import React, { useState } from 'react';
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css';
import RangeSlider from 'react-bootstrap-range-slider';
const axios = require('axios').default;
const format = 'HH:mm';

class Locations extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value:0,startValue: '', endValue: '', timeValue:0, parkCost:0, parkDep:0, parkEta:0, payCost:0, payDep:0, payEta:0, prayCost:0, prayDep:0, prayEta:0};
    // const [ value, setValue ] = useState(40); 
    this.sliderValue = {slider:40} 
    this.handleChangeStart = this.handleChangeStart.bind(this);
    this.handleChangeEnd = this.handleChangeEnd.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChangeTime = this.handleChangeTime.bind(this);
  }
  
  handleChangeStart(event) {
    // alert(this.state.startValue)
    this.setState({startValue: event.target.value});
  }

  handleChangeEnd(event) {
    // alert(this.state.endValue)
    this.setState({endValue: event.target.value});
  }

  handleChangeTime(timeToArrive) {
    if (timeToArrive != null){
      var hoursToMin = timeToArrive.hours() * 60
      var min = timeToArrive.minutes() 
      this.setState({timeValue: hoursToMin + min})
    }
  }


  handleSubmit(event){
    axios.post('http://localhost:5000/routes_options/by_address', {
      "source":  this.state.startValue,
      "target": this.state.endValue,
      "latest_arrival_time": this.state.timeValue
    })
    .then(function (response) { 
      console.log(response)
      this.setState({parkCost: response.data.park_result.cost})
      this.setState({parkDep: response.data.park_result.start_time})
      this.setState({parkEta: response.data.park_result.end_time})
      this.setState({payCost: response.data.pay_result.cost})
      this.setState({payDep: response.data.pay_result.start_time})
      this.setState({payEta: response.data.pay_result.end_time})
      this.setState({prayCost: response.data.pray_result.cost})
      this.setState({prayDep: response.data.pray_result.start_time})
      this.setState({prayEta: response.data.pray_result.end_time})
    }.bind(this))
    .catch(function (error) {
      console.log(error);
    });
  }

  convertMin(mint) {
    var h = Math.floor(mint / 60);
    var m = mint % 60;
    h = h < 10 ? '0' + h : h; 
    m = m < 10 ? '0' + m : m; 
    return h + ':' + m;
  }

  render() {
    
    return (
      <div className="MainDiv" >
        <br></br>
        <InputGroup className="mb-3 shadow-sm mx-auto InputBox w-25">
        <InputGroup.Text id="Start" >Start</InputGroup.Text>
        <FormControl aria-label="Default" aria-describedby="Start" value={this.state.startValue} onChange={this.handleChangeStart} />
        </InputGroup>
        <br></br>
        <InputGroup className="mb-3 shadow-sm mx-auto InputBox w-25" >
        <InputGroup.Text id="end">End</InputGroup.Text>
        <FormControl aria-label="Default" aria-describedby="end" value={this.state.endValue} onChange={this.handleChangeEnd} />
        </InputGroup>
              <br></br>
        <label>Latest time to arrive: &nbsp;</label>
        <TimePicker defaultValue={moment('12:08', format)}  className="locations"  onChange={this.handleChangeTime} format={format} /> 
        <br></br>
        <br></br>
        <div className="container">
  <div className="row mx-auto">
  <div className="col-3"></div>
    <div className="col-1">
    <InputGroup className="mb-3  mx-auto  w-25" > <Form.Label> Cost</Form.Label> </InputGroup>
    </div>
    <div className="col-4">
    <RangeSlider
            value={this.sliderValue.value}
            onChange={e => this.setState({value : e})}
          />
    </div>
    <div className="col-sm">
      Time
    </div>
  </div>
</div>
<InputGroup className="mb-3  mx-auto  w-25" >
   <Button variant="success" onClick={this.handleSubmit} className='mx-auto'>Go!</Button></InputGroup>

   <InputGroup className="mb-3  mx-auto  w-25" >
    <Card style={{ width: '20rem' }} className="bg-warning">
  <Card.Body>
    <Card.Title>Park</Card.Title>
    <Card.Text>
      Total Cost:
      <br/>
      {Math.round(this.state.parkCost)}
      <br/>
      Departure Time:
      <br/>
      {this.convertMin(Math.round(this.state.parkDep))}
      <br/>
      ETA:
      <br/>
      {this.convertMin(Math.round(this.state.parkEta))}
    </Card.Text>
  </Card.Body>
</Card>
<Card style={{ width: '20rem' }} className="bg-danger">
  <Card.Body>
    <Card.Title>Pay</Card.Title>
    <Card.Text>
    Total Cost:
      <br/>
       {Math.round(this.state.payCost)}
      <br/>
      Departure Time:
      <br/>
      {this.convertMin(Math.round(this.state.payDep))}
      <br/>
      ETA:
      <br/>
      {this.convertMin(Math.round(this.state.payEta))}
    </Card.Text>
  </Card.Body>
</Card> 
<Card style={{ width: '20rem' }} className="bg-success">
  <Card.Body>
    <Card.Title>Pray</Card.Title>
    <Card.Text>
      Total Cost:
      <br/>
      {Math.round(this.state.prayCost)}
      <br/>
      Departure Time:
      <br/>
      {this.convertMin(Math.round(this.state.prayDep))}
      <br/>
      ETA:
      <br/>
      {this.convertMin(Math.round(this.state.prayEta))}
    </Card.Text>
  </Card.Body>
</Card>
</InputGroup>
      </div>
    );
  }
}


export {Locations };
