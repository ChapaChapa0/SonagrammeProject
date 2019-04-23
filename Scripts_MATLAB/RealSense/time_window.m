function windowT = time_window(LS_base, old_i, pas_t)

n = length(LS_base);

if old_i <= pas_t
    if old_i > n - pas_t
        windowT = [1, n];
    else
        windowT = [1, old_i + pas_t];
    end
else
    if old_i > n - pas_t
        windowT = [old_i - pas_t, n];
    else
        windowT = [old_i - pas_t, old_i + pas_t];
    end
end