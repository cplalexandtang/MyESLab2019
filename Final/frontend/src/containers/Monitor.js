import React, { Component } from 'react';
import { Card, Button, CardTitle, CardText, Row, Col, ListGroup, ListGroupItem, Table } from 'reactstrap';

const axios = require('axios');

export default class Monitor extends Component {
  constructor(props) {
    super(props);
    this.state = {
      waiting: [],
      now: undefined
    };
  }

  handleNext = () => {
    let newState = { ...this.state };
    newState.now = newState.waiting.shift();
    console.log(newState);
    this.setState(newState)
  }

  handleWake = () => {
    if (this.state.now)
      alert(this.state.now);
    else
      alert("no people");
  }

  update = () => {
    axios.get("https://bypasscors.herokuapp.com/api/?url=https://2e37c514.ngrok.io/status")
      .then(res => {
        this.setState(() => {
          return {
            now: res.data.waiting_list.shift(),
            waiting: res.data.waiting_list
          }
        })
      })
      .catch(err=>{
        console.log(err)
      })
  }

  componentDidMount() {
    //setInterval(() => this.update(), 5000);
  }

  render() {
    return (
      <div>
        <h1> Moniter </h1>
        <Row style={{ height: "400px" }}>
          <Col xs="6">
            <Card body outline color="primary" style={{ height: "400px" }}>
              <CardText tag="h2">
                {
                  this.state.now ? this.state.now : "no people"
                }
              </CardText>
            </Card>
          </Col>
          <Col xs="6" style={{ height: "400px", overflow: "auto" }}>
            <Table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>id</th>
                </tr>
              </thead>
              <tbody>
                {
                  this.state.waiting.map((e, id) => {
                    return (
                      <tr key={id}>
                        <th scope="row">{id}</th>
                        <td>{e}</td>
                      </tr>
                    )
                  })
                }
              </tbody>
            </Table>
          </Col>
        </Row>
        <br />
        <Button outline color="primary" onClick={this.handleWake}>叫號</Button>{" "}
        <Button outline color="secondary" onClick={this.handleNext}>下一位</Button>
      </div>
    );
  }
}
