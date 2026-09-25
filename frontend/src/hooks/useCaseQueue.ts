import { useQuery } from '@tanstack/react-query';

import { fetchCases } from '../api';

export function useCaseQueue() {
  return useQuery({
    queryKey: ['cases'],
    queryFn: fetchCases,
    retry: 1,
  });
}
