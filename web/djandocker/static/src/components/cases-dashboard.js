import _ from 'lodash';
import React from 'react';
import CasesDashboardHeader from './cases-dashboard-header';
import CaseItem from './case-item.js';

export default class CasesDashboard extends React.Component {
    renderCases() {
        return _.map(this.props.cases, (caseItem, index) => <CaseItem key={index} {...caseItem} />);
    }

    render() {
        return (
            <table>
                <CasesDashboardHeader />
                <tbody>
                    {this.renderCases()}
                </tbody>
            </table>
        );
    }
}
