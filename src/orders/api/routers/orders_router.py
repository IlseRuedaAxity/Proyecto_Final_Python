from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.orders.api.auth import get_current_user
from src.orders.api.dependencies import (
    get_create_order_use_case,
    get_get_order_use_case,
    get_order_repository,
)
from src.orders.api.schemas.order_schemas import (
    ErrorResponse,
    OrderIn,
    OrderListResponse,
    OrderOut,
)
from src.orders.application.dtos.order_dtos import CreateOrderDTO, CreateOrderItemDTO
from src.orders.application.use_cases.create_order import CreateOrderUseCase
from src.orders.application.use_cases.get_order import GetOrderUseCase

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post(
    "",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}},
)
async def create_order(
    payload: OrderIn,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
    current_user: dict = Depends(get_current_user),
):
    """Crear una nueva orden"""
    try:
        dto = CreateOrderDTO(
            customer_id=payload.customer_id,
            customer_name=payload.customer_name,
            items=[
                CreateOrderItemDTO(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    quantity=i.quantity,
                    unit_price=i.unit_price,
                )
                for i in payload.items
            ],
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "errorCode": "ORD_001",
                "errorMessage": str(e),
                "userError": "Error al crear la orden",
            },
        )


@router.get("/{order_id}", response_model=OrderOut, responses={404: {"model": ErrorResponse}})
async def get_order(
    order_id: UUID,
    use_case: GetOrderUseCase = Depends(get_get_order_use_case),
    current_user: dict = Depends(get_current_user),
):
    """Obtener una orden por ID"""
    result = await use_case.execute(order_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "errorCode": "ORD_404",
                "errorMessage": "Order not found",
                "userError": "Orden no encontrada",
            },
        )
    return result


@router.get("", response_model=OrderListResponse)
async def list_orders(
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    repo=Depends(get_order_repository),
    current_user: dict = Depends(get_current_user),
):
    """Listar órdenes con paginación"""
    orders = await repo.get_all(limit=limit, offset=offset)
    results = [
        OrderOut(
            id=o.id,
            customer_id=o.customer_id,
            customer_name=o.customer_name,
            status=o.status.value,
            total=o.total(),
            items_count=len(o.items),
        )
        for o in orders
    ]
    return OrderListResponse(data=results, total=len(results), limit=limit, offset=offset)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: UUID,
    repo=Depends(get_order_repository),
    current_user: dict = Depends(get_current_user),
):
    """Eliminar una orden"""
    deleted = await repo.delete(order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
