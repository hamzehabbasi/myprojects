from AppBase.usage import usage
from Business.models import SubscriptionService, SubscriptionServiceCostModel


@usage
def delete_service_v1abcd12(_, d, device):
    if 'Validate Request and Initialize':
        try:
            customer = device.user

            service = SubscriptionService.ag(key__exact=d['key'], provider__customer__exact=customer)
            _ = service.key
        except (ValueError, KeyError, AttributeError):
            return 400

    if 'Check For Already Deleted':
        if service.trashed:
            return 200

    if 'Clean Uploaded Image':
        if service.image and service.image.url.startswith("https"):
            service.image.delete(save=True)

    if 'Delete':
        cost_models = service.cost_models.all()
        for cost_model in cost_models:
            cost_model.trashed = True
        SubscriptionServiceCostModel.objects.bulk_update(cost_models, ['trashed'])

        service.trashed = True
        service.save()
    # if "Delete Customer Group":
    #     group = CustomerGroup.f(title=service.title)
    #     group.trashed = True
    #     group.save()

    return 200
