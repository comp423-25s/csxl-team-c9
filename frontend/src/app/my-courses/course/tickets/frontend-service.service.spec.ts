import { TestBed } from '@angular/core/testing';

import { FrontendServiceService } from './frontend-service.service';

describe('FrontendServiceService', () => {
  let service: FrontendServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FrontendServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
