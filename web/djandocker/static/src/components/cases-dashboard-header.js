import React from 'react';

export default class CasesDashboardHeader extends React.Component {
    render() {
        return (
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Policy Number</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
        );
    }
}
