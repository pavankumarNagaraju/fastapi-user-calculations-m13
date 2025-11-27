from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/calculations", tags=["calculations"])


def perform_operation(operation: str, a: float, b: float) -> float:
    op = operation.lower()
    if op == "add":
        return a + b
    elif op == "subtract":
        return a - b
    elif op == "multiply":
        return a * b
    elif op == "divide":
        if b == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot divide by zero",
            )
        return a / b
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported operation",
        )


# BROWSE
@router.get("/", response_model=list[schemas.CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    return db.query(models.Calculation).all()


# READ
@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    return calc


# ADD
@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    result = perform_operation(calc_in.operation, calc_in.operand1, calc_in.operand2)
    calc = models.Calculation(
        operation=calc_in.operation,
        operand1=calc_in.operand1,
        operand2=calc_in.operand2,
        result=result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


# EDIT
@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def edit_calculation(
    calc_id: int,
    calc_update: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    if calc_update.operation is not None:
        calc.operation = calc_update.operation
    if calc_update.operand1 is not None:
        calc.operand1 = calc_update.operand1
    if calc_update.operand2 is not None:
        calc.operand2 = calc_update.operand2

    calc.result = perform_operation(calc.operation, calc.operand1, calc.operand2)

    db.commit()
    db.refresh(calc)
    return calc


# DELETE
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return None
