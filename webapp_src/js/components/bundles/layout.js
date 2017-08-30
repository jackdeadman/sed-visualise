import React from 'react';

export const Page = props => (
    <div class="page-inner">
        { props.children }
    </div>
);

export const Overhang = props => (
    <div class="overhang cf">
          <Page>
            { props.children }
          </Page>
    </div>
);
