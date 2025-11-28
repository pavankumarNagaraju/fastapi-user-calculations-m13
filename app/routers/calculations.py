from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


def _compute_result(operand1: float, operand2: float, operation: str) -> float:
    if operation == "add":
        return operand1 + operand2
    if operation == "subtract":
        return operand1 - operand2
    if operation == "multiply":
        return operand1 * operand2
    if operation == "divide":
        if operand2 == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot divide by zero",
            )
        return operand1 / operand2

    # This is what test_invalid_operation_returns_error expects (400)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid operation",
    )


@router.post(
    "/",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation(
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    """
    POST /calculations

    Used by test_calculation_bread_flow:
    - Creates a calculation
    - Stores result in DB
    - Returns 201 + CalculationRead
    """
    result = _compute_result(
        calc_in.operand1,
        calc_in.operand2,
        calc_in.operation,
    )

    calc = models.Calculation(
        operand1=calc_in.operand1,
        operand2=calc_in.operand2,
        operation=calc_in.operation,
        result=result,
        created_at=datetime.utcnow(),
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.get(
    "/",
    response_model=List[schemas.CalculationRead],
)
def list_calculations(db: Session = Depends(get_db)):
    """
    GET /calculations
    Returns all calculations.
    """
    return db.query(models.Calculation).all()


@router.get(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
)
def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    """
    GET /calculations/{id}
    """
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@router.put(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
)
def update_calculation(
    calc_id: int,
    calc_in: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    """
    PUT /calculations/{id}
    Updates operands/operation and recomputes result.
    """
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    if calc_in.operand1 is not None:
        calc.operand1 = calc_in.operand1
    if calc_in.operand2 is not None:
        calc.operand2 = calc_in.operand2
    if calc_in.operation is not None:
        calc.operation = calc_in.operation

    calc.result = _compute_result(
        calc.operand1,
        calc.operand2,
        calc.operation,
    )

    db.commit()
    db.refresh(calc)
    return calc


@router.delete("/{calc_id}")
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    """
    DELETE /calculations/{id}
    Returns 200 + simple detail message.
    """
    calc = db.query(models.Calculation).get(calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return {"detail": "Calculation deleted"}
