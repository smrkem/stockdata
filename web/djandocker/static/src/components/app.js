import React from 'react';
import CasesDashboard from './cases-dashboard';

// Mock data:
const cases = [
{
  "case_id": 1,
  "client_data": {
    "first_name": "John",
    "id": 1,
    "last_name": "Testcase",
    "url": "http://localhost:5000/api/v1life-insured/1"
  },
  "client_system_id": null,
  "hq_url": "http://localhost:5000/api/v1/cases/1/hq/"
},
{
  "case_id": 2,
  "client_data": {
    "first_name": "Mark",
    "id": 2,
    "last_name": "Smith",
    "url": "http://localhost:5000/api/v1life-insured/2"
  },
  "client_system_id": null,
  "hq_url": "http://localhost:5000/api/v1/cases/2/hq/"
}
];

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            cases
        };
    }

    render() {
        return (
            <div>
                <h1>Cases Dashboard</h1>
                <CasesDashboard cases={this.state.cases} />
            </div>
        );
    }
}
