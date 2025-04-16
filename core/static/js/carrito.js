$(document).ready(function() {
    // Incrementar cantidad
    $('.quantity-btn:contains("+")').click(function() {
        const input = $(this).siblings('.quantity-input');
        let value = parseInt(input.val());
        input.val(value + 1);
        updateSubtotal($(this).closest('tr'));
    });

    // Decrementar cantidad
    $('.quantity-btn:contains("-")').click(function() {
        const input = $(this).siblings('.quantity-input');
        let value = parseInt(input.val());
        if (value > 1) {
            input.val(value - 1);
            updateSubtotal($(this).closest('tr'));
        }
    });

    // Eliminar producto
    $('.remove-btn').click(function() {
        $(this).closest('tr').remove();
        updateTotal();
        
        // Mostrar mensaje de carrito vacío si no hay productos
        if ($('.cart-table tbody tr').length === 0) {
            $('.table-responsive').hide();
            $('.total-section').hide();
            $('.empty-cart').show();
        }
    });

    // Actualizar subtotal de un producto
    function updateSubtotal(row) {
        const price = parseInt(row.find('td:nth-child(2)').text().replace('$', '').replace('.', ''));
        const quantity = parseInt(row.find('.quantity-input').val());
        const subtotal = price * quantity;
        row.find('td:nth-child(4)').text('$' + subtotal.toLocaleString());
        updateTotal();
    }

    // Actualizar total del carrito
    function updateTotal() {
        let total = 0;
        $('.cart-table tbody tr').each(function() {
            const subtotalText = $(this).find('td:nth-child(4)').text().replace('$', '').replace('.', '');
            total += parseInt(subtotalText);
        });
        
        const shipping = 5000;
        const discount = 0;
        const subtotal = total;
        total = subtotal + shipping - discount;
        
        $('.total-section .d-flex:nth-child(1) span:last-child').text('$' + subtotal.toLocaleString());
        $('.total-section .d-flex:nth-child(3) span:last-child').text('$' + shipping.toLocaleString());
        $('.total-section .d-flex:nth-child(5) strong:last-child').text('$' + total.toLocaleString());
    }
});