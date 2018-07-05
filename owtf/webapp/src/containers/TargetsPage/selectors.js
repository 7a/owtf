/**
 * The target state selectors
 */

import { createSelector } from 'reselect';

const selectTarget = (state) => state.get('targets');

const makeSelectFetch = createSelector(
  selectTarget,
  (targetState) => targetState.get('load')
);

const makeSelectCreate = createSelector(
  selectTarget,
  (targetState) => targetState.get('create')
);

const makeSelectFetchLoading = createSelector(
  makeSelectFetch,
  (fetchState) => fetchState.get('loading')
);

const makeSelectFetchError = createSelector(
  makeSelectFetch,
  (fetchState) => fetchState.get('error')
);

const makeSelectFetchTargets = createSelector(
  makeSelectFetch,
  (fetchState) => fetchState.get('targets')
);

const makeSelectCreateLoading = createSelector(
  makeSelectCreate,
  (fetchState) => fetchState.get('loading')
);
  
const makeSelectCreateError = createSelector(
  makeSelectCreate,
  (fetchState) => fetchState.get('error')
);

export {
  makeSelectFetchLoading,
  makeSelectFetchError,
  makeSelectFetchTargets,
  makeSelectCreateLoading,
  makeSelectCreateError,
};