import React from 'react';

export default class CaseItem extends React.Component {
    handleStartHQ(event) {
        event.preventDefault();
        $.ajax({
            url: '/aj_start_hq',
            dataType: 'json',
            cache: false,
            success: (data) => {
                alert('got data');
                console.log(data);
            },
            error: (xhr, status, err) => {
                console.log(xhr.statusText);
                alert('error retrieving start_hq response.');
            }
        });
    }

    render() {
        return (
            <tr>
                <td>{this.props.case_id}</td>
                <td>P{this.props.client_data.id}-{this.props.case_id}L</td>
                <td>{this.props.client_data.first_name}</td>
                <td>{this.props.client_data.last_name}</td>
                <td><button onClick={this.handleStartHQ}>Start HQ</button></td>
            </tr>
        );
    }
}
