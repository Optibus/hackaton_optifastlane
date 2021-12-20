
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

function fetchData(){
  axios.post('http://localhost:5000/routes_options', {
    "source_lon": 34.835387,
    "source_lat": 32.008449,
    "target_lon": 34.900114,
    "target_lat": 31.967937
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
}

function Locations() {
  return (
    <div className="MainDiv" >
      <br></br>
      <InputGroup className="mb-3 shadow-sm mx-auto InputBox w-25">
      <InputGroup.Text id="inputGroup-sizing-default">Start</InputGroup.Text>
      <FormControl aria-label="Default" aria-describedby="inputGroup-sizing-default" />
      </InputGroup>
      <InputGroup className="mb-3 shadow-sm mx-auto InputBox w-25" >
      <InputGroup.Text id="inputGroup-sizing-default">End</InputGroup.Text>
      <FormControl aria-label="Default" aria-describedby="inputGroup-sizing-default" />
      </InputGroup>
      <label>Latest time to arrive: &nbsp;</label>
      <TimePicker defaultValue={moment('12:08', format)}  className="locations"  format={format} /> 
    </div>
  );
}

function Slider(){
  const [ value, setValue ] = useState(40); 
  return(  <div className="container">
  <div className="row mx-auto">
    <div className="col-1">
    <InputGroup className="mb-3  mx-auto  w-25" > <Form.Label> Cost</Form.Label> </InputGroup>
    </div>
    <div className="col-4">
    <RangeSlider
            value={value}
            onChange={e => setValue(e.target.value)}
          />
    </div>
    <div className="col-sm">
      Time
    </div>
  </div>
</div>
)



}

function ButtonGo(){
  
  return  (
  <InputGroup className="mb-3  mx-auto  w-25" >
   <Button variant="success" onClick={fetchData} className='mx-auto'>Go!</Button></InputGroup>
  ) 
}

function Cards(){
  return(
    <InputGroup className="mb-3  mx-auto  w-25" >
    <Card style={{ width: '20rem' }} className="bg-warning">
  <Card.Body>
    <Card.Title>Park</Card.Title>
    <Card.Text>
      Total Cost
      <br/>
      -total_cost-
      <br/>
      Total Time
      <br/>
      -total_time-
      <br/>
      Total CO2 Emissions
      <br/>
      -total_co2-
    </Card.Text>
  </Card.Body>
</Card>
<Card style={{ width: '20rem' }} className="bg-danger">
  <Card.Body>
    <Card.Title>Pay</Card.Title>
    <Card.Text>
      Total Cost
      <br/>
      -total_cost-
      <br/>
      Total Time
      <br/>
      -total_time-
      <br/>
      Total CO2 Emissions
      <br/>
      -total_co2-
    </Card.Text>
  </Card.Body>
</Card>
<br/>
<Card style={{ width: '20rem' }} className="bg-success">
  <Card.Body>
    <Card.Title>Pray</Card.Title>
    <Card.Text>
      Total Cost
      <br/>
      -total_cost-
      <br/>
      Total Time
      <br/>
      -total_time-
      <br/>
      Total CO2 Emissions
      <br/>
      -total_co2-
    </Card.Text>
  </Card.Body>
</Card>
</InputGroup>
  )
}
export {Locations, Cards, Slider, ButtonGo };
