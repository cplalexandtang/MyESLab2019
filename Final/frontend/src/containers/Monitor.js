import React, { Component } from 'react';
import { Card, Button, CardText, Row, Col, Table } from 'reactstrap';

const axios = require('axios');

export default class Monitor extends Component {
  constructor(props) {
    super(props);
    this.state = {
      waiting_list: [],
      now: undefined
    };
  }

  handleNext = () => {
    let newState = { ...this.state };
    axios.delete("http://localhost:9487/delete/" + this.state.now)
      .then(res => {
        console.log(res);
      })
      .catch(err => {
        console.log(err)
      })
    newState.now = newState.waiting_list.shift();
    console.log(newState);
    this.setState(newState)
  }

  handleWake = () => {
    axios.get("http://localhost:9487/call/" + this.state.now)
      .then(res => console.log(res))
      .catch(err => console.log(err))

    if (this.state.now)
      alert(this.state.now);
    else
      alert("no people");
  }

  update = () => {
    axios.get("http://localhost:9487/status")
      .then(res => {
        this.setState(() => {
          console.log(res.data)
          if (res.data.waiting_list.length >= 0)
            return {
              now: res.data.waiting_list.shift(),
              waiting_list: res.data.waiting_list
            }
        })
      })
      .catch(err => {
        console.log(err)
      })
  }

  componentDidMount() {
    this.update();
    setInterval(() => this.update(), 1000);
  }

  render() {
    return (
      <div>
        <h4> Moniter </h4>
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
                  this.state.waiting_list.map((e, id) => {
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
