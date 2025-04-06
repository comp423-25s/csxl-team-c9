import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssignmentsConceptsPageComponent } from './assignments-concepts-page.component';

describe('AssignmentsConceptsPageComponent', () => {
  let component: AssignmentsConceptsPageComponent;
  let fixture: ComponentFixture<AssignmentsConceptsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssignmentsConceptsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AssignmentsConceptsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
