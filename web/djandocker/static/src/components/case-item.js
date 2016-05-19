import React from 'react';

export default class CaseItem extends React.Component {
    render() {
        return (
            <tr>
                <td>{this.props.case_id}</td>
                <td>P{this.props.client_data.id}-{this.props.case_id}L</td>
                <td>{this.props.client_data.first_name}</td>
                <td>{this.props.client_data.last_name}</td>
                <td><button>Start HQ</button></td>
            </tr>
        );
    }
}
