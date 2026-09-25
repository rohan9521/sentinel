import { useQuery } from '@tanstack/react-query';

import { fetchResults } from '../api';

export function useResults() {
  return useQuery({
    queryKey: ['results'],
    queryFn: fetchResults,
    retry: 1,
  });
}
